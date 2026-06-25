from __future__ import annotations

import json
import re
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


ENDPOINT = "https://resume-ai-agent-resource.services.ai.azure.com/api/projects/Resume_AI_Agent"
JOB_DESCRIPTION_DIR = Path("job-description")
OUTPUT_DIR = Path("outputs") / "step1"
MODEL = "gpt-4.1-mini"


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
        endpoint=ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    return project_client


def parse_job_description(job_description: str) -> dict:
    project_client = build_job_parser_client()
    openai_client = project_client.get_openai_client()
    response = openai_client.responses.create(
        model=MODEL,
        input=job_description,
        text={
            "format": {
                "type": "json_schema",
                "name": "job_parser_output",
                "schema": {
                    "type": "object",
                    "properties": {
                        "company_name": {"type": "string"},
                        "role_title": {"type": "string"},
                        "role_level": {"type": "string"},
                        "employment_type": {"type": "string"},
                        "location": {"type": "string"},
                        "salary_range": {"type": ["string", "null"]},
                        "tech_stack": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "count": {"type": "integer"},
                                    "relevance_score": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 5,
                                    },
                                },
                                "required": [
                                    "name",
                                    "count",
                                    "relevance_score",
                                ],
                                "additionalProperties": False,
                            },
                        },
                        "required_skills": {"type": "array", "items": {"type": "string"}},
                        "preferred_skills": {"type": "array", "items": {"type": "string"}},
                        "responsibilities": {"type": "array", "items": {"type": "string"}},
                        "qualifications": {"type": "array", "items": {"type": "string"}},
                        "industry": {"type": "string"},
                        "ats_keywords": {"type": "array", "items": {"type": "string"}},
                        "company_values": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": [
                        "company_name",
                        "role_title",
                        "role_level",
                        "employment_type",
                        "location",
                        "salary_range",
                        "tech_stack",
                        "required_skills",
                        "preferred_skills",
                        "responsibilities",
                        "qualifications",
                        "industry",
                        "ats_keywords",
                        "company_values",
                    ],
                    "additionalProperties": False,
                },
            },
        },
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
