from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from Agents.output_paths import OUTPUT_ROOT_DIR, get_step_output_path
from Agents.project_config import (
    get_experience_matcher_agent_name,
    get_experience_matcher_endpoint,
)

EXPERIENCE_PATH = Path("Data") / "experience.json"
OUTPUT_DIR = OUTPUT_ROOT_DIR


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def keyword_set(values: Iterable[str]) -> set[str]:
    return {normalize_text(value) for value in values if value}


def score_fact(fact: str, job_terms: set[str], job_phrases: set[str]) -> int:
    fact_text = normalize_text(fact)
    score = 0

    for phrase in job_phrases:
        if phrase and phrase in fact_text:
            score += 4

    for term in job_terms:
        if term and term in fact_text:
            score += 1

    return score


def score_fact_against_job(fact: str, job_description: dict) -> int:
    tech_stack_items = job_description.get("tech_stack", [])
    tech_stack = {normalize_text(item["name"]) for item in tech_stack_items}
    required_skills = keyword_set(job_description.get("required_skills", []))
    preferred_skills = keyword_set(job_description.get("preferred_skills", []))
    responsibilities = keyword_set(job_description.get("responsibilities", []))
    qualifications = keyword_set(job_description.get("qualifications", []))
    ats_keywords = keyword_set(job_description.get("ats_keywords", []))

    tech_weights = {
        normalize_text(item["name"]): int(item.get("relevance_score", 0))
        for item in tech_stack_items
    }
    job_terms = tech_stack | required_skills | preferred_skills | ats_keywords
    job_phrases = responsibilities | qualifications
    score = score_fact(fact, job_terms, job_phrases)

    fact_text = normalize_text(fact)
    for tech_name, relevance_score in tech_weights.items():
        if tech_name and tech_name in fact_text:
            score += relevance_score

    return score


def rank_experience_facts(experiences: list[dict], job_description: dict) -> list[dict]:
    ranked_experiences: list[dict] = []

    for experience in experiences:
        scored_facts = [
            {
                "fact": fact,
                "score": score_fact_against_job(fact, job_description),
            }
            for fact in experience.get("facts", [])
        ]
        scored_facts.sort(key=lambda item: item["score"], reverse=True)
        top_facts = scored_facts[:4]
        ranked_experiences.append(
            {
                "id": experience["id"],
                "company": experience["company"],
                "role": experience["role"],
                "facts": top_facts,
                "total_score": sum(item["score"] for item in top_facts),
            }
        )

    ranked_experiences.sort(key=lambda item: item["total_score"], reverse=True)
    return ranked_experiences


def build_next_agent_payload(ranked_experiences: list[dict]) -> list[dict]:
    return [
        {
            "id": experience["id"],
            "company": experience["company"],
            "role": experience["role"],
            "facts": [
                {
                    "text": item["fact"],
                    "score": item["score"],
                }
                for item in experience["facts"]
            ],
        }
        for experience in ranked_experiences
    ]


def build_experience_matcher_client() -> AIProjectClient:
    return AIProjectClient(
        endpoint=get_experience_matcher_endpoint(),
        credential=DefaultAzureCredential(),
        allow_preview=True,
    )


def match_experience_facts(
    ranked_experiences: list[dict],
    job_parser_output: dict,
) -> list[dict]:
    next_agent_input = build_next_agent_payload(ranked_experiences)
    project_client = build_experience_matcher_client()
    openai_client = project_client.get_openai_client(agent_name=get_experience_matcher_agent_name())
    response = openai_client.responses.create(
        input=json.dumps(
            {
                "job_parser_output": job_parser_output,
                "ranked_experiences": next_agent_input,
            }
        ),
    )
    return json.loads(response.output_text)["matched_experiences"]


def write_experience_matcher_output(source_file: Path, matched_experiences: list[dict]) -> Path:
    output_path = get_step_output_path(source_file, "step2")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(matched_experiences, indent=2), encoding="utf-8")
    return output_path


def run_experience_matcher(source_file: Path, job_parser_output: dict) -> tuple[Path, list[dict]]:
    experiences = json.loads(EXPERIENCE_PATH.read_text(encoding="utf-8"))
    ranked_experiences = rank_experience_facts(experiences, job_parser_output)
    matched_experiences = match_experience_facts(ranked_experiences, job_parser_output)
    output_path = write_experience_matcher_output(source_file, matched_experiences)
    return output_path, matched_experiences
