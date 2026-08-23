from __future__ import annotations

import json
from pathlib import Path

from Agents.experience_matcher import run_experience_matcher
from Agents.job_parser import (
    JOB_DESCRIPTION_DIR,
    OUTPUT_DIR as STEP1_OUTPUT_DIR,
    find_latest_text_file,
    load_parsed_job_description,
    parse_latest_job_description,
    write_parsed_job_description,
)
from Agents.experience_matcher import OUTPUT_DIR as STEP2_OUTPUT_DIR
from Agents.project_matcher import OUTPUT_DIR as STEP3_OUTPUT_DIR, run_project_matcher
from Agents.resume_renderer import render_resume


def run_job_parser() -> tuple[Path, dict]:
    source_file = find_latest_text_file(JOB_DESCRIPTION_DIR)
    fallback_output_path = STEP1_OUTPUT_DIR / f"{source_file.stem}.json"
    if fallback_output_path.exists():
        parsed_output = load_parsed_job_description(fallback_output_path)
        return source_file, parsed_output

    try:
        source_file, parsed_output = parse_latest_job_description()
        write_parsed_job_description(source_file, parsed_output)
        return source_file, parsed_output
    except Exception:
        if not fallback_output_path.exists():
            raise
        parsed_output = load_parsed_job_description(fallback_output_path)
        return source_file, parsed_output


def run_experience_matching(source_file: Path, parsed_job_description: dict) -> list[dict]:
    fallback_output_path = STEP2_OUTPUT_DIR / f"{source_file.stem}.json"
    if fallback_output_path.exists():
        return json.loads(fallback_output_path.read_text(encoding="utf-8"))

    try:
        _, matched_experiences = run_experience_matcher(source_file, parsed_job_description)
        return matched_experiences
    except Exception:
        if not fallback_output_path.exists():
            raise
        return json.loads(fallback_output_path.read_text(encoding="utf-8"))


def run_next_step(source_file: Path, parsed_job_description: dict) -> tuple[Path | None, Path | None]:
    fallback_output_path = STEP3_OUTPUT_DIR / f"{source_file.stem}.json"
    if not fallback_output_path.exists():
        try:
            run_project_matcher(source_file, parsed_job_description)
        except Exception:
            if not fallback_output_path.exists():
                raise
    return render_resume(source_file, parsed_job_description)


def main() -> None:
    source_file, parsed_job_description = run_job_parser()
    run_experience_matching(source_file, parsed_job_description)
    tex_path, pdf_path = run_next_step(source_file, parsed_job_description)
    if pdf_path is None:
        print(f"Rendered resume template: {tex_path}")
        print("PDF build skipped: no LaTeX compiler found. Install `pdflatex`, `tectonic`, or `latexmk`.")
    else:
        print(f"Built PDF: {pdf_path}")


if __name__ == "__main__":
    main()
