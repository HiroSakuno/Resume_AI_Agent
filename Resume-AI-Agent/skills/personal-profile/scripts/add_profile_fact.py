from __future__ import annotations

import sys
from datetime import date
from pathlib import Path


SECTIONS = {
    "profile": "profile.md",
    "experience": "experience.md",
    "tech-stack": "tech-stack.md",
    "projects": "projects.md",
    "education": "education.md",
    "languages": "languages.md",
}


def knowledge_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "knowledge"


def append_fact(section: str, fact: str) -> Path:
    if section not in SECTIONS:
        valid_sections = ", ".join(SECTIONS)
        raise ValueError(f"Unknown section: {section}. Valid sections: {valid_sections}.")

    clean_fact = fact.strip()
    if not clean_fact:
        raise ValueError("Fact cannot be empty.")

    section_path = knowledge_dir() / SECTIONS[section]
    entry = f"\n\n## Added Facts\n\n- {date.today().isoformat()}: {clean_fact}\n"

    existing_content = section_path.read_text(encoding="utf-8")
    if "## Added Facts" in existing_content:
        updated_content = existing_content.rstrip() + f"\n- {date.today().isoformat()}: {clean_fact}\n"
    else:
        updated_content = existing_content.rstrip() + entry

    section_path.write_text(updated_content, encoding="utf-8")
    return section_path


def main() -> int:
    if len(sys.argv) != 3:
        valid_sections = ", ".join(SECTIONS)
        print(
            "Error: expected exactly two arguments: <section> <fact>. "
            f"Valid sections: {valid_sections}.",
            file=sys.stderr,
        )
        return 2

    section, fact = sys.argv[1], sys.argv[2]
    try:
        section_path = append_fact(section, fact)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print(f"Added fact to {section_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
