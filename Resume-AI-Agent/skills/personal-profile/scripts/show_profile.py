from __future__ import annotations

import sys
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


def selected_sections(args: list[str]) -> list[str]:
    if not args:
        return list(SECTIONS)

    invalid_sections = [section for section in args if section not in SECTIONS]
    if invalid_sections:
        valid_sections = ", ".join(SECTIONS)
        invalid = ", ".join(invalid_sections)
        raise ValueError(f"Unknown section(s): {invalid}. Valid sections: {valid_sections}.")

    return args


def read_section(section: str) -> str:
    section_path = knowledge_dir() / SECTIONS[section]
    return section_path.read_text(encoding="utf-8").strip()


def main() -> int:
    try:
        sections = selected_sections(sys.argv[1:])
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print("\n\n".join(read_section(section) for section in sections))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
