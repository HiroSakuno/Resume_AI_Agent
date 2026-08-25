from __future__ import annotations

from pathlib import Path


OUTPUT_ROOT_DIR = Path("outputs")
RESUME_FILE_STEM = "Resume - Hiro Sakuno"


def get_job_output_dir(source_file: Path) -> Path:
    return OUTPUT_ROOT_DIR / source_file.stem


def get_step_output_path(source_file: Path, step_name: str) -> Path:
    return get_job_output_dir(source_file) / f"{step_name}.json"


def get_resume_tex_path(source_file: Path) -> Path:
    return get_job_output_dir(source_file) / f"{RESUME_FILE_STEM}.tex"
