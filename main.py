from __future__ import annotations

from pathlib import Path

from Agents.experience_matcher import run_experience_matcher
from Agents.job_parser import (
    parse_latest_job_description,
    write_parsed_job_description,
)


def run_job_parser() -> tuple[Path, dict]:
    source_file, parsed_output = parse_latest_job_description()
    write_parsed_job_description(source_file, parsed_output)
    return source_file, parsed_output


def run_next_step() -> None:
    return None


def main() -> None:
    source_file, parsed_job_description = run_job_parser()
    run_experience_matcher(source_file, parsed_job_description)
    run_next_step()


if __name__ == "__main__":
    main()
