from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


EXPERIENCE_PATH = Path("Data") / "experience.json"
OUTPUT_DIR = Path("outputs") / "step2"
ENDPOINT = "https://resume-ai-agent-resource.services.ai.azure.com/api/projects/Resume_AI_Agent"
MODEL = "gpt-4.1-mini"


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
                "skills": experience.get("skills", []),
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
            "skills": experience["skills"],
        }
        for experience in ranked_experiences
    ]


def build_experience_matcher_client() -> AIProjectClient:
    return AIProjectClient(
        endpoint=ENDPOINT,
        credential=DefaultAzureCredential(),
    )


def match_experience_facts(
    ranked_experiences: list[dict],
    job_parser_output: dict,
) -> list[dict]:
    next_agent_input = build_next_agent_payload(ranked_experiences)
    project_client = build_experience_matcher_client()
    openai_client = project_client.get_openai_client()
    response = openai_client.responses.create(
        model=MODEL,
        input=[
            {
                "type": "message",
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You rank resume experience facts for a job description. "
                            "Return only the provided JSON schema."
                        ),
                    }
                ],
            },
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(
                            {
                                "job_parser_output": job_parser_output,
                                "ranked_experiences": next_agent_input,
                            }
                        ),
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "experience_matcher_output",
                "schema": {
                    "type": "object",
                    "properties": {
                        "matched_experiences": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "company": {"type": "string"},
                                    "role": {"type": "string"},
                                    "selected_facts": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": [
                                    "id",
                                    "company",
                                    "role",
                                    "selected_facts",
                                    "skills",
                                ],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["matched_experiences"],
                    "additionalProperties": False,
                },
            },
        },
    )
    return json.loads(response.output_text)["matched_experiences"]


def write_experience_matcher_output(source_file: Path, matched_experiences: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{source_file.stem}.json"
    output_path.write_text(json.dumps(matched_experiences, indent=2), encoding="utf-8")
    return output_path


def run_experience_matcher(source_file: Path, job_parser_output: dict) -> tuple[Path, list[dict]]:
    experiences = json.loads(EXPERIENCE_PATH.read_text(encoding="utf-8"))
    ranked_experiences = rank_experience_facts(experiences, job_parser_output)
    matched_experiences = match_experience_facts(ranked_experiences, job_parser_output)
    output_path = write_experience_matcher_output(source_file, matched_experiences)
    return output_path, matched_experiences
