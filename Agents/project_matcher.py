from __future__ import annotations

import json
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from Agents.project_config import (
    get_project_matcher_agent_name,
    get_project_matcher_endpoint,
)

PROJECTS_PATH = Path("Data") / "projects.json"
OUTPUT_DIR = Path("outputs") / "step3"


def load_projects_payload() -> dict:
    return json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))


def build_project_matcher_client() -> AIProjectClient:
    return AIProjectClient(
        endpoint=get_project_matcher_endpoint(),
        credential=DefaultAzureCredential(),
        allow_preview=True,
    )


def match_projects(job_parser_output: dict, projects_payload: dict) -> dict:
    project_client = build_project_matcher_client()
    openai_client = project_client.get_openai_client(agent_name=get_project_matcher_agent_name())
    response = openai_client.responses.create(
        input=json.dumps(
            {
                "job_parser_output": job_parser_output,
                "projects": projects_payload.get("projects", []),
            }
        ),
    )
    return json.loads(response.output_text)


def write_project_matcher_output(source_file: Path, matched_projects: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{source_file.stem}.json"
    output_path.write_text(json.dumps(matched_projects, indent=2), encoding="utf-8")
    return output_path


def run_project_matcher(source_file: Path, job_parser_output: dict) -> tuple[Path, dict]:
    projects_payload = load_projects_payload()
    matched_projects = match_projects(job_parser_output, projects_payload)
    output_path = write_project_matcher_output(source_file, matched_projects)
    return output_path, matched_projects
