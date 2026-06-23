from __future__ import annotations

import json
from pathlib import Path

from Agents.experience_matcher import run_experience_matcher
from Agents.job_parser import (
    parse_latest_job_description,
    write_parsed_job_description,
)


def run_job_parser() -> tuple[Path, dict]:
    source_file, parsed_output = parse_latest_job_description()
    output_path = write_parsed_job_description(source_file, parsed_output)

    print(f"Selected file: {source_file.name}")
    print(f"Saved JSON to: {output_path}")
    print(json.dumps(parsed_output, indent=2))
    return output_path, parsed_output


def run_next_step() -> None:
    msg = "Next step is not implemented yet."
    print(msg)


def main() -> None:
    _, parsed_job_description = run_job_parser()
    run_experience_matcher(parsed_job_description)
    run_next_step()


if __name__ == "__main__":
    main()
