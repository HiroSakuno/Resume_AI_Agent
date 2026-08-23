from __future__ import annotations

import os
from pathlib import Path


AZURE_AI_PROJECT_ENDPOINT_ENV_VAR = "AZURE_AI_PROJECT_ENDPOINT"
AZURE_AI_JOB_PARSER_ENDPOINT_ENV_VAR = "AZURE_AI_JOB_PARSER_ENDPOINT"
AZURE_AI_EXPERIENCE_MATCHER_ENDPOINT_ENV_VAR = "AZURE_AI_EXPERIENCE_MATCHER_ENDPOINT"
AZURE_AI_PROJECT_MATCHER_ENDPOINT_ENV_VAR = "AZURE_AI_PROJECT_MATCHER_ENDPOINT"
AZURE_AI_JOB_PARSER_AGENT_NAME_ENV_VAR = "AZURE_AI_JOB_PARSER_AGENT_NAME"
AZURE_AI_EXPERIENCE_MATCHER_AGENT_NAME_ENV_VAR = "AZURE_AI_EXPERIENCE_MATCHER_AGENT_NAME"
AZURE_AI_PROJECT_MATCHER_AGENT_NAME_ENV_VAR = "AZURE_AI_PROJECT_MATCHER_AGENT_NAME"
DEFAULT_PROJECT_MATCHER_ENDPOINT = "https://resume-ai-agent-resource.services.ai.azure.com/api/projects/Resume_AI_Agent"
DEFAULT_PROJECT_MATCHER_AGENT_NAME = "Project-Matcher"
ROOT_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = ROOT_DIR / ".env"


def load_dotenv_value(variable_name: str) -> str:
    if not DOTENV_PATH.exists():
        return ""

    for raw_line in DOTENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        if key.strip() != variable_name:
            continue

        cleaned_value = value.strip().strip("'\"")
        if cleaned_value:
            return cleaned_value

    return ""


def load_config_value(variable_name: str) -> str:
    value = os.getenv(variable_name, "").strip()
    if not value:
        value = load_dotenv_value(variable_name)
    return value


def get_required_config_value(
    primary_variable_name: str,
    fallback_variable_name: str | None = None,
    config_label: str = "configuration value",
) -> str:
    value = load_config_value(primary_variable_name)
    if not value and fallback_variable_name:
        value = load_config_value(fallback_variable_name)
    if value:
        return value

    if fallback_variable_name:
        raise RuntimeError(
            f"Missing {config_label}. "
            f"Set {primary_variable_name} or {fallback_variable_name} in the environment "
            "or local .env file before running the resume pipeline."
        )

    raise RuntimeError(
        f"Missing {config_label}. "
        f"Set the {primary_variable_name} environment variable "
        "or add it to the local .env file before running the resume pipeline."
    )


def get_azure_ai_project_endpoint() -> str:
    endpoint = get_required_config_value(
        AZURE_AI_PROJECT_ENDPOINT_ENV_VAR,
        config_label="Azure AI Project endpoint",
    )
    return endpoint


def get_job_parser_endpoint() -> str:
    return get_required_config_value(
        AZURE_AI_JOB_PARSER_ENDPOINT_ENV_VAR,
        fallback_variable_name=AZURE_AI_PROJECT_ENDPOINT_ENV_VAR,
        config_label="Job-Parser endpoint",
    )


def get_experience_matcher_endpoint() -> str:
    return get_required_config_value(
        AZURE_AI_EXPERIENCE_MATCHER_ENDPOINT_ENV_VAR,
        fallback_variable_name=AZURE_AI_PROJECT_ENDPOINT_ENV_VAR,
        config_label="Experience-Matcher endpoint",
    )


def get_job_parser_agent_name() -> str:
    return get_required_config_value(
        AZURE_AI_JOB_PARSER_AGENT_NAME_ENV_VAR,
        config_label="Job-Parser agent name",
    )


def get_experience_matcher_agent_name() -> str:
    return get_required_config_value(
        AZURE_AI_EXPERIENCE_MATCHER_AGENT_NAME_ENV_VAR,
        config_label="Experience-Matcher agent name",
    )


def get_project_matcher_endpoint() -> str:
    endpoint = load_config_value(AZURE_AI_PROJECT_MATCHER_ENDPOINT_ENV_VAR)
    if endpoint:
        return endpoint
    return DEFAULT_PROJECT_MATCHER_ENDPOINT


def get_project_matcher_agent_name() -> str:
    agent_name = load_config_value(AZURE_AI_PROJECT_MATCHER_AGENT_NAME_ENV_VAR)
    if agent_name:
        return agent_name
    return DEFAULT_PROJECT_MATCHER_AGENT_NAME
