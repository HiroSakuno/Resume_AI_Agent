from __future__ import annotations

import json
import re
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from Agents.project_config import get_job_parser_agent_name, get_job_parser_endpoint

JOB_DESCRIPTION_DIR = Path("job-description")
OUTPUT_DIR = Path("outputs") / "step1"


def find_latest_text_file(directory: Path) -> Path:
    candidates: list[tuple[int, Path]] = []

    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = re.match(r"^(\d+)-", path.name)
        if match:
            candidates.append((int(match.group(1)), path))

    if not candidates:
        raise FileNotFoundError(f"No numbered .txt files found in {directory}")

    return max(candidates, key=lambda item: item[0])[1]


def build_job_parser_client() -> AIProjectClient:
    project_client = AIProjectClient(
        endpoint=get_job_parser_endpoint(),
        credential=DefaultAzureCredential(),
        allow_preview=True,
    )
    return project_client


def parse_job_description(job_description: str) -> dict:
    project_client = build_job_parser_client()
    openai_client = project_client.get_openai_client(agent_name=get_job_parser_agent_name())
    response = openai_client.responses.create(
        input=job_description,
    )
    return json.loads(response.output_text)


def parse_latest_job_description() -> tuple[Path, dict]:
    latest_file = find_latest_text_file(JOB_DESCRIPTION_DIR)
    job_description = latest_file.read_text(encoding="utf-8")
    parsed_output = parse_job_description(job_description)
    return latest_file, parsed_output


def write_parsed_job_description(source_file: Path, parsed_output: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{source_file.stem}.json"
    output_path.write_text(json.dumps(parsed_output, indent=2), encoding="utf-8")
    return output_path


def load_parsed_job_description(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
