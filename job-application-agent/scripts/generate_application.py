#!/usr/bin/env python3
"""
Job Application Generator — main entry point.
Usage:
    python scripts/generate_application.py --job job_descriptions/raw/job_001.txt
    python scripts/generate_application.py --job-text "paste job description here"
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

import anthropic
import yaml
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE_DIR = BASE_DIR / "profile"
TEMPLATES_DIR = BASE_DIR / "templates"
PROMPTS_DIR = BASE_DIR / "prompts"
OUTPUTS_DIR = BASE_DIR / "outputs"
JOB_PARSED_DIR = BASE_DIR / "job_descriptions" / "parsed"

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8192


# ---------------------------------------------------------------------------
# Helpers — file loading
# ---------------------------------------------------------------------------

def load_env():
    """Load .env from project root."""
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return api_key


def load_yaml(filename: str) -> dict:
    """Load a YAML file from the profile directory."""
    path = PROFILE_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompt(filename: str) -> str:
    """Load a prompt markdown file."""
    path = PROMPTS_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_template(filename: str) -> str:
    """Load a template markdown file."""
    path = TEMPLATES_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_job_description(args) -> str:
    """Load job description from file or CLI argument."""
    if args.job_text:
        return args.job_text.strip()
    elif args.job:
        path = Path(args.job)
        if not path.is_absolute():
            path = BASE_DIR / path
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        print("ERROR: Provide --job <path> or --job-text <text>")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers — Claude API calls
# ---------------------------------------------------------------------------

def call_claude(client: anthropic.Anthropic, prompt: str, step_name: str) -> str:
    """
    Call Claude API with a single user message.
    Returns the text response.
    """
    print(f"  → Calling Claude for: {step_name} ...", end="", flush=True)

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    if response.stop_reason == "refusal":
        print(f" REFUSED")
        raise RuntimeError(f"Claude refused request at step '{step_name}'. Check prompt content.")

    text = ""
    for block in response.content:
        if block.type == "text":
            text += block.text

    print(f" done ({response.usage.output_tokens} tokens)")
    return text.strip()


def parse_json_response(text: str, step_name: str) -> dict:
    """Parse JSON from a Claude response, with cleanup for common issues."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last fence lines
        cleaned = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\nWARNING: JSON parse failed at step '{step_name}': {e}")
        print(f"Raw response (first 500 chars): {text[:500]}")
        raise


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def step_01_parse_job(client, job_text: str) -> dict:
    """Step 1: Parse the raw job description into structured JSON."""
    prompt_template = load_prompt("01_parse_job.md")
    prompt = prompt_template.format(job_description_text=job_text)
    response_text = call_claude(client, prompt, "01 Parse Job Description")
    return parse_json_response(response_text, "01_parse_job")


def step_02_select_experience(client, parsed_job: dict, profile: dict) -> dict:
    """Step 2: Select most relevant experience and skills for this role."""
    prompt_template = load_prompt("02_select_relevant_experience.md")
    prompt = prompt_template.format(
        experience_json=json.dumps(profile["experience"], indent=2, ensure_ascii=False),
        projects_json=json.dumps(profile["projects"], indent=2, ensure_ascii=False),
        skills_json=json.dumps(profile["skills"], indent=2, ensure_ascii=False),
        achievements_json=json.dumps(profile["achievements"], indent=2, ensure_ascii=False),
        certifications_json=json.dumps(profile["certifications"], indent=2, ensure_ascii=False),
        parsed_job_json=json.dumps(parsed_job, indent=2, ensure_ascii=False),
    )
    response_text = call_claude(client, prompt, "02 Select Relevant Experience")
    return parse_json_response(response_text, "02_select_experience")


def step_03_generate_resume(
    client, parsed_job: dict, selection: dict, profile: dict
) -> str:
    """Step 3: Generate the tailored resume in Markdown."""
    # Build selected experience objects
    experiences = profile["experience"]
    if isinstance(experiences, dict) and "experience" in experiences:
        experiences = experiences["experience"]
    exp_map = {e["id"]: e for e in experiences if isinstance(e, dict) and "id" in e}
    selected_ids = selection.get("selected_experience_ids", [])
    selected_exp = [exp_map[eid] for eid in selected_ids if eid in exp_map]

    projects = profile["projects"]
    if isinstance(projects, dict) and "projects" in projects:
        projects = projects["projects"]
    project_map = {p["id"]: p for p in projects if isinstance(p, dict) and "id" in p}
    selected_project_ids = selection.get("selected_project_ids", [])
    selected_projects = [
        project_map[project_id]
        for project_id in selected_project_ids
        if project_id in project_map
    ]

    prompt_template = load_prompt("03_generate_resume.md")
    prompt = prompt_template.format(
        master_profile_json=json.dumps(profile["master"], indent=2, ensure_ascii=False),
        selection_json=json.dumps(selection, indent=2, ensure_ascii=False),
        selected_experience_json=json.dumps(selected_exp, indent=2, ensure_ascii=False),
        selected_projects_json=json.dumps(selected_projects, indent=2, ensure_ascii=False),
        parsed_job_json=json.dumps(parsed_job, indent=2, ensure_ascii=False),
        resume_template=load_template("resume_template.md"),
        keywords_to_embed=", ".join(selection.get("keywords_to_embed", [])),
    )
    return call_claude(client, prompt, "03 Generate Resume")


def step_04_generate_cover_letter(
    client, parsed_job: dict, selection: dict, profile: dict
) -> str:
    """Step 4: Generate the tailored cover letter in Markdown."""
    prompt_template = load_prompt("04_generate_cover_letter.md")
    prompt = prompt_template.format(
        master_profile_json=json.dumps(profile["master"], indent=2, ensure_ascii=False),
        selection_json=json.dumps(selection, indent=2, ensure_ascii=False),
        parsed_job_json=json.dumps(parsed_job, indent=2, ensure_ascii=False),
        cover_letter_template=load_template("cover_letter_template.md"),
    )
    return call_claude(client, prompt, "04 Generate Cover Letter")


def step_05_ats_review(
    client, parsed_job: dict, resume_md: str
) -> str:
    """Step 5: Run ATS keyword analysis against the generated resume."""
    prompt_template = load_prompt("05_ats_review.md")
    prompt = prompt_template.format(
        generated_resume=resume_md,
        parsed_job_json=json.dumps(parsed_job, indent=2, ensure_ascii=False),
        ats_review_template=load_template("ats_review_template.md"),
    )
    return call_claude(client, prompt, "05 ATS Review")


def step_06_quality_check(
    client, parsed_job: dict, resume_md: str, cover_letter_md: str, ats_report: str
) -> str:
    """Step 6: Final quality check of the complete application package."""
    # Provide a concise ATS summary (first 2000 chars to save tokens)
    ats_summary = ats_report[:2000] + ("..." if len(ats_report) > 2000 else "")
    prompt_template = load_prompt("06_final_quality_check.md")
    prompt = prompt_template.format(
        generated_resume=resume_md,
        generated_cover_letter=cover_letter_md,
        parsed_job_json=json.dumps(parsed_job, indent=2, ensure_ascii=False),
        ats_report_summary=ats_summary,
    )
    return call_claude(client, prompt, "06 Final Quality Check")


# ---------------------------------------------------------------------------
# Output management
# ---------------------------------------------------------------------------

def create_output_dir(parsed_job: dict) -> Path:
    """Create timestamped output directory: outputs/company_role_YYYY-MM-DD/"""
    company = parsed_job.get("company_name", "unknown_company")
    role = parsed_job.get("role_title", "unknown_role")
    today = date.today().strftime("%Y-%m-%d")

    # Sanitize folder name
    def sanitize(s: str) -> str:
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in s.replace(" ", "_"))

    folder_name = f"{sanitize(company)}_{sanitize(role)}_{today}"
    output_dir = OUTPUTS_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_outputs(
    output_dir: Path,
    parsed_job: dict,
    selection: dict,
    resume_md: str,
    cover_letter_md: str,
    ats_report: str,
    quality_check: str,
):
    """Save all generated outputs as .md files."""
    files = {
        "resume.md": resume_md,
        "cover_letter.md": cover_letter_md,
        "ats_report.md": ats_report,
        "quality_check.md": quality_check,
        "parsed_job.json": json.dumps(parsed_job, indent=2, ensure_ascii=False),
        "selection_strategy.json": json.dumps(selection, indent=2, ensure_ascii=False),
    }
    for filename, content in files.items():
        path = output_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Saved: {path.relative_to(BASE_DIR)}")

    # Also save a copy of the job to parsed/
    JOB_PARSED_DIR.mkdir(parents=True, exist_ok=True)
    parsed_path = JOB_PARSED_DIR / f"parsed_{date.today().strftime('%Y%m%d')}_{output_dir.name}.json"
    with open(parsed_path, "w", encoding="utf-8") as f:
        json.dump(parsed_job, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_documents(output_dir: Path):
    """Call export scripts for DOCX and PDF."""
    import subprocess

    resume_path = output_dir / "resume.md"
    cover_path = output_dir / "cover_letter.md"
    export_script_docx = BASE_DIR / "scripts" / "export_docx.py"
    export_script_pdf = BASE_DIR / "scripts" / "export_pdf.py"

    print("\n[Exporting DOCX...]")
    result = subprocess.run(
        [sys.executable, str(export_script_docx),
         str(resume_path), str(cover_path), str(output_dir)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  WARNING: DOCX export had issues:\n{result.stderr}")
    else:
        print(f"  DOCX export complete.")

    print("\n[Exporting PDF...]")
    result = subprocess.run(
        [sys.executable, str(export_script_pdf),
         str(resume_path), str(cover_path), str(output_dir)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  WARNING: PDF export had issues:\n{result.stderr}")
    else:
        print(f"  PDF export complete.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_all_profiles() -> dict:
    """Load all YAML profile files into a single dict."""
    return {
        "master": load_yaml("master_profile.yaml"),
        "experience": load_yaml("experience.yaml"),
        "skills": load_yaml("skills.yaml"),
        "certifications": load_yaml("certifications.yaml"),
        "education": load_yaml("education.yaml"),
        "achievements": load_yaml("achievements.yaml"),
        "projects": load_yaml("projects.yaml"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="AI Job Application Generator — generates resume, cover letter, and ATS report"
    )
    parser.add_argument(
        "--job", type=str,
        help="Path to a .txt file containing the job description"
    )
    parser.add_argument(
        "--job-text", type=str,
        help="Paste job description as a string directly"
    )
    parser.add_argument(
        "--no-export", action="store_true",
        help="Skip DOCX/PDF export (generate .md only)"
    )
    args = parser.parse_args()

    # ---- Setup ----
    api_key = load_env()
    client = anthropic.Anthropic(api_key=api_key)
    job_text = load_job_description(args)
    profile = load_all_profiles()

    print("\n========================================")
    print("  AI Job Application Generator")
    print("========================================\n")
    print(f"Model: {MODEL}")
    print(f"Job text length: {len(job_text)} characters\n")

    # ---- Pipeline ----
    print("[Step 1/6] Parsing job description...")
    parsed_job = step_01_parse_job(client, job_text)
    print(f"  Company: {parsed_job.get('company_name', 'N/A')}")
    print(f"  Role:    {parsed_job.get('role_title', 'N/A')}")

    print("\n[Step 2/6] Selecting relevant experience...")
    selection = step_02_select_experience(client, parsed_job, profile)
    print(f"  Selected experience IDs: {selection.get('selected_experience_ids', [])}")
    if selection.get("skill_gaps"):
        print(f"  Skill gaps noted: {selection['skill_gaps']}")

    print("\n[Step 3/6] Generating tailored resume...")
    resume_md = step_03_generate_resume(client, parsed_job, selection, profile)

    print("\n[Step 4/6] Generating cover letter...")
    cover_letter_md = step_04_generate_cover_letter(client, parsed_job, selection, profile)

    print("\n[Step 5/6] Running ATS keyword analysis...")
    ats_report = step_05_ats_review(client, parsed_job, resume_md)

    print("\n[Step 6/6] Final quality check...")
    quality_check = step_06_quality_check(
        client, parsed_job, resume_md, cover_letter_md, ats_report
    )

    # ---- Save outputs ----
    print("\n[Saving outputs...]")
    output_dir = create_output_dir(parsed_job)
    print(f"  Output folder: {output_dir.relative_to(BASE_DIR)}")
    save_outputs(
        output_dir, parsed_job, selection,
        resume_md, cover_letter_md, ats_report, quality_check
    )

    # ---- Export ----
    if not args.no_export:
        export_documents(output_dir)

    print("\n========================================")
    print(f"  Done! Application saved to:")
    print(f"  {output_dir}")
    print("========================================\n")

    # Print quality check summary
    print("=== Quality Check Summary ===")
    print(quality_check[:1000])
    if len(quality_check) > 1000:
        print("... (see quality_check.md for full report)")


if __name__ == "__main__":
    main()
