from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


PROFILE_PATH = Path("Data") / "profile.json"
EXPERIENCE_PATH = Path("Data") / "experience.json"
PROJECTS_PATH = Path("Data") / "projects.json"
EDUCATION_PATH = Path("Data") / "education.json"
LANGUAGES_PATH = Path("Data") / "languages.json"
STEP1_DIR = Path("outputs") / "step1"
STEP2_DIR = Path("outputs") / "step2"
OUTPUT_DIR = Path("outputs") / "step3"
TEMPLATE_PATH = Path("main.tex")
JOB_DESCRIPTION_DIR = Path("job-description")


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def find_latest_text_file(directory: Path) -> Path:
    candidates: list[tuple[int, Path]] = []
    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = re.match(r"^(\d+)-", path.name)
        if match:
            candidates.append((int(match.group(1)), path))

    if not candidates:
        raise FileNotFoundError(f"No numbered files found in {directory}")

    return max(candidates, key=lambda item: item[0])[1]


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    escaped_parts: list[str] = []
    for character in value:
        escaped_parts.append(replacements.get(character, character))
    return "".join(escaped_parts)


def format_secondary_text(value: str) -> str:
    escaped_value = latex_escape(value)
    return escaped_value.replace("|", r"\textbar{}")


def format_contact_link(url: str, label: str) -> str:
    return f"\\resumeContactLink{{{url}}}{{{latex_escape(label)}}}"


def format_bullet_items(items: list[str]) -> str:
    if not items:
        return ""

    lines = ["\\resumeItemListStart"]
    for item in items:
        lines.append(f"\\resumeItem{{{latex_escape(item)}}}")
    lines.append("\\resumeItemListEnd")
    return "\n".join(lines)


def get_render_options(profile: dict) -> dict:
    return profile.get("render_options", {})


def format_contact_line(profile: dict) -> str:
    contact = profile.get("contact", {})
    manual_line = contact.get("contact_line_latex", "").strip()
    if manual_line:
        return manual_line

    contact_items: list[str] = []
    phone = contact.get("phone", "").strip()
    if phone:
        phone_target = re.sub(r"[^\d+]", "", phone)
        if phone_target:
            contact_items.append(format_contact_link(f"tel:{phone_target}", phone))
        else:
            contact_items.append(latex_escape(phone))

    email = contact.get("email", "").strip()
    if email:
        contact_items.append(format_contact_link(f"mailto:{email}", email))

    linkedin_url = contact.get("linkedin_url", "").strip()
    linkedin_label = contact.get("linkedin_label", "").strip()
    if linkedin_url:
        visible_linkedin = linkedin_label or linkedin_url.removeprefix("https://").removeprefix("http://")
        contact_items.append(format_contact_link(linkedin_url, visible_linkedin))

    portfolio_url = contact.get("portfolio_url", "").strip()
    portfolio_label = contact.get("portfolio_label", "").strip()
    if portfolio_url:
        visible_portfolio = portfolio_label or portfolio_url.removeprefix("https://").removeprefix("http://")
        contact_items.append(format_contact_link(portfolio_url, visible_portfolio))

    if contact_items:
        return " ~|~ ".join(contact_items)

    fallback_values = [
        profile.get("core_identity", {}).get("location", "").strip(),
        profile.get("core_identity", {}).get("professional_headline", "").strip(),
    ]
    fallback_text = next((value for value in fallback_values if value), "")
    return latex_escape(fallback_text)


def format_experience_entries(
    matched_experiences: list[dict],
    all_experiences: list[dict],
    max_bullets: int,
) -> str:
    experiences_by_id = {experience["id"]: experience for experience in all_experiences}
    experience_order = {experience["id"]: index for index, experience in enumerate(all_experiences)}
    ordered_matches = sorted(
        matched_experiences,
        key=lambda experience: experience_order.get(experience["id"], len(all_experiences)),
    )

    blocks: list[str] = []
    for matched_experience in ordered_matches:
        source_experience = experiences_by_id.get(matched_experience["id"])
        if source_experience is None:
            continue

        selected_facts = matched_experience.get("selected_facts", [])[:max_bullets]
        blocks.append(
            "\n".join(
                [
                    "\\resumeSubheading",
                    f"  {{{latex_escape(source_experience['company'])}}}{{{latex_escape(source_experience.get('period', ''))}}}",
                    f"  {{{format_secondary_text(source_experience['role'])}}}{{}}",
                    format_bullet_items(selected_facts),
                ]
            )
        )

    return "\n\n".join(block for block in blocks if block)


def format_experience_section(
    matched_experiences: list[dict],
    all_experiences: list[dict],
    max_bullets: int,
) -> str:
    entries = format_experience_entries(matched_experiences, all_experiences, max_bullets)
    if not entries:
        return ""

    return "\n".join(
        [
            "%-----------EXPERIENCE-----------",
            "\\section{Experience}",
            "  \\resumeSubHeadingListStart",
            entries,
            "  \\resumeSubHeadingListEnd",
            "\\vspace{-16pt}",
        ]
    )


def format_projects_entries(projects_payload: dict, max_heading_technologies: int) -> str:
    project_items = projects_payload.get("projects", [])
    blocks: list[str] = []
    for project in project_items:
        heading_technologies = project.get("resume_heading_technologies") or project.get("technologies", [])[
            :max_heading_technologies
        ]
        derived_subtitle = ", ".join(heading_technologies)

        project_links: list[str] = []
        github_url = project.get("github_url", "").strip()
        if github_url:
            project_links.append(f"\\href{{{github_url}}}{{\\underline{{GitHub}}}}")

        demo_url = project.get("demo_url", "").strip()
        if demo_url:
            project_links.append(f"\\href{{{demo_url}}}{{\\underline{{Demo}}}}")

        resume_bullets = project.get("resume_bullets", [])
        if resume_bullets:
            bullet_items = [bullet for bullet in resume_bullets if bullet]
        else:
            bullets = [project.get("summary", ""), project.get("purpose", "")]
            bullet_items = [bullet for bullet in bullets if bullet]

        project_title = latex_escape(project.get("resume_title", project["name"]))
        project_date = latex_escape(project.get("resume_date", project.get("date", "")).strip())
        project_subtitle = project.get("resume_subtitle", "").strip() or derived_subtitle
        project_meta = project.get("resume_meta", "").strip()
        if project_meta:
            project_meta_text = format_secondary_text(project_meta)
        else:
            project_meta_text = " ~|~ ".join(project_links)

        blocks.append(
            "\n".join(
                [
                    "\\resumeSubheading",
                    f"  {{{project_title}}}{{{project_date}}}",
                    f"  {{{format_secondary_text(project_subtitle)}}}{{{project_meta_text}}}",
                    format_bullet_items(bullet_items),
                ]
            )
        )

    return "\n\n".join(block for block in blocks if block)


def format_projects_section(projects_payload: dict, max_heading_technologies: int) -> str:
    entries = format_projects_entries(projects_payload, max_heading_technologies=max_heading_technologies)
    if not entries:
        return ""

    return "\n".join(
        [
            "%-----------PROJECTS-----------",
            "\\section{Projects}",
            "  \\resumeSubHeadingListStart",
            entries,
            "  \\resumeSubHeadingListEnd",
            "\\vspace{-16pt}",
        ]
    )


def format_certifications_and_languages_lines(education_payload: dict, languages_payload: dict) -> str:
    lines: list[str] = []

    certifications = education_payload.get("certifications", [])
    if certifications:
        certification_names = [certification["name"] for certification in certifications if certification.get("name")]
        if certification_names:
            lines.append(f"    \\textbf{{Certifications}}: {latex_escape(', '.join(certification_names))} \\\\")

    spoken_languages = languages_payload.get("spoken_languages", [])
    if spoken_languages:
        language_items = [
            f"{language['language']} ({language['proficiency']})"
            for language in spoken_languages
        ]
        if language_items:
            lines.append(f"    \\textbf{{Languages}}: {latex_escape(', '.join(language_items))} \\\\")

    return "\n".join(lines).rstrip("\\")


def format_certifications_and_languages_section(education_payload: dict, languages_payload: dict) -> str:
    section_lines = format_certifications_and_languages_lines(education_payload, languages_payload)
    if not section_lines:
        return ""

    return "\n".join(
        [
            "%-----------CERTIFICATIONS AND LANGUAGES-----------",
            "\\section{Certifications and Languages}",
            " \\begin{itemize}[leftmargin=0.15in, label={}]",
            "    \\small{\\item{",
            section_lines,
            "    }}",
            " \\end{itemize}",
            " \\vspace{-16pt}",
        ]
    )


def format_education_entries(education_payload: dict) -> str:
    blocks: list[str] = []
    for education in education_payload.get("formal_education", []):
        blocks.append(
            "\n".join(
                [
                    "\\resumeSubheading",
                    f"  {{{latex_escape(education['institution'])}}}{{{latex_escape(str(education.get('graduation_year', '')))}}}",
                    f"  {{{format_secondary_text(education['degree'])}}}{{{format_secondary_text(education.get('location', ''))}}}",
                ]
            )
        )

    return "\n\n".join(blocks)


def format_education_section(education_payload: dict) -> str:
    entries = format_education_entries(education_payload)
    if not entries:
        return ""

    return "\n".join(
        [
            "%-----------EDUCATION-----------",
            "\\section{Education}",
            "  \\resumeSubHeadingListStart",
            entries,
            "  \\resumeSubHeadingListEnd",
        ]
    )


def format_certifications_entries(education_payload: dict) -> str:
    blocks: list[str] = []
    for certification in education_payload.get("certifications", []):
        status = certification.get("status", "").title()
        issuer = certification.get("issuer", "")
        subtitle_parts = [part for part in [issuer, status] if part]
        subtitle = " | ".join(subtitle_parts)
        blocks.append(
            "\n".join(
                [
                    "\\resumeSubheading",
                    f"  {{{latex_escape(certification['name'])}}}{{{latex_escape(str(certification.get('year', '')))}}}",
                    f"  {{{format_secondary_text(subtitle)}}}{{}}",
                ]
            )
        )

    return "\n\n".join(blocks)


def format_certifications_section(education_payload: dict, include_section: bool) -> str:
    if not include_section:
        return ""

    entries = format_certifications_entries(education_payload)
    if not entries:
        return ""

    return "\n".join(
        [
            "%-----------CERTIFICATIONS-----------",
            "\\section{Certifications}",
            "  \\resumeSubHeadingListStart",
            entries,
            "  \\resumeSubHeadingListEnd",
            "\\vspace{-14pt}",
        ]
    )


def format_languages_line(languages_payload: dict) -> str:
    spoken_languages = languages_payload.get("spoken_languages", [])
    formatted_languages = [
        f"{language['language']} ({language['proficiency']})"
        for language in spoken_languages
    ]
    return latex_escape(", ".join(formatted_languages))


def format_languages_section(languages_payload: dict, include_section: bool) -> str:
    if not include_section:
        return ""

    languages_line = format_languages_line(languages_payload)
    if not languages_line:
        return ""

    return "\n".join(
        [
            "%-----------LANGUAGES-----------",
            "\\section{Languages}",
            "\\begin{itemize}[leftmargin=0.15in, label={}]",
            f"  \\small{{\\item{{{languages_line}}}}}",
            "\\end{itemize}",
        ]
    )


def fill_template(template: str, replacements: dict[str, str]) -> str:
    rendered_template = template
    for placeholder, value in replacements.items():
        rendered_template = rendered_template.replace(placeholder, value)
    return rendered_template


def find_latex_compiler() -> tuple[str, list[str]] | None:
    if shutil.which("pdflatex"):
        return "pdflatex", ["pdflatex", "-interaction=nonstopmode", "-halt-on-error"]
    if shutil.which("tectonic"):
        return "tectonic", ["tectonic"]
    if shutil.which("latexmk"):
        return "latexmk", ["latexmk", "-pdf"]
    return None


def build_pdf(tex_path: Path) -> Path:
    compiler = find_latex_compiler()
    if compiler is None:
        raise RuntimeError(
            "No LaTeX compiler found. Install `pdflatex`, `tectonic`, or `latexmk` to build the PDF."
        )

    absolute_tex_path = tex_path.resolve()
    output_directory = absolute_tex_path.parent
    compiler_name, command = compiler
    if compiler_name == "pdflatex":
        compile_command = [*command, "-output-directory", str(output_directory), absolute_tex_path.name]
    elif compiler_name == "tectonic":
        compile_command = [*command, "--outdir", str(output_directory), absolute_tex_path.name]
    else:
        compile_command = [*command, f"-output-directory={output_directory}", absolute_tex_path.name]

    subprocess.run(
        compile_command,
        check=True,
        cwd=output_directory,
    )

    pdf_path = absolute_tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF output was not created: {pdf_path}")
    return pdf_path


def try_build_pdf(tex_path: Path) -> Path | None:
    if find_latex_compiler() is None:
        return None
    return build_pdf(tex_path)


def render_resume(source_file: Path, job_parser_output: dict) -> tuple[Path, Path | None]:
    profile = load_json(PROFILE_PATH)
    all_experiences = load_json(EXPERIENCE_PATH)
    projects_payload = load_json(PROJECTS_PATH)
    education_payload = load_json(EDUCATION_PATH)
    languages_payload = load_json(LANGUAGES_PATH)
    matched_experiences = load_json(STEP2_DIR / f"{source_file.stem}.json")
    render_options = get_render_options(profile)
    max_experience_bullets = render_options.get("max_experience_bullets", 3)
    max_project_heading_technologies = render_options.get("max_project_heading_technologies", 4)
    include_certifications_section = render_options.get("include_certifications_section", False)
    include_languages_section = render_options.get("include_languages_section", False)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "PLACEHOLDERFULLNAME": latex_escape(profile["core_identity"]["name"]),
        "PLACEHOLDERCONTACTLINE": format_contact_line(profile),
        "PLACEHOLDEREDUCATIONSECTION": format_education_section(education_payload),
        "PLACEHOLDEREXPERIENCESECTION": format_experience_section(
            matched_experiences,
            all_experiences,
            max_bullets=max_experience_bullets,
        ),
        "PLACEHOLDERPROJECTSSECTION": format_projects_section(
            projects_payload,
            max_heading_technologies=max_project_heading_technologies,
        ),
        "PLACEHOLDERSKILLSSECTION": format_certifications_and_languages_section(
            education_payload,
            languages_payload,
        ),
        "PLACEHOLDERCERTIFICATIONSSECTION": "",
        "PLACEHOLDERLANGUAGESSECTION": "",
    }
    rendered_resume = fill_template(template, replacements)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUTPUT_DIR / f"{source_file.stem}.tex"
    tex_path.write_text(rendered_resume, encoding="utf-8")

    pdf_path = try_build_pdf(tex_path)
    return tex_path, pdf_path


def render_latest_resume() -> tuple[Path, Path | None]:
    source_file = find_latest_text_file(JOB_DESCRIPTION_DIR)
    job_parser_output = load_json(STEP1_DIR / f"{source_file.stem}.json")
    return render_resume(source_file, job_parser_output)


if __name__ == "__main__":
    render_latest_resume()
