# Personal Profile Skill

Use this skill whenever the user asks about Hiro's background, resume, projects, education, technical stack, languages, career story, interview preparation, portfolio content, or professional biography.

## Knowledge Sources

Read the markdown files in `knowledge/` before answering profile-specific questions:

- `knowledge/profile.md`: identity, positioning, summaries, and preferences.
- `knowledge/experience.md`: roles, responsibilities, achievements, and impact.
- `knowledge/tech-stack.md`: programming languages, frameworks, platforms, data tools, AI tools, and proficiency notes.
- `knowledge/projects.md`: portfolio, academic, professional, and personal projects.
- `knowledge/education.md`: schools, degrees, certifications, courses, and learning history.
- `knowledge/languages.md`: spoken languages and communication strengths.

## How To Answer

- Ground claims in the knowledge files.
- If a fact is missing or marked `TODO`, say what information is needed instead of guessing.
- Prefer concise, polished professional wording that can be reused in resumes, LinkedIn, bios, recruiter messages, and interview answers.
- Preserve Hiro's voice where preferences are documented.
- When writing resume bullets, use observable impact and concrete technologies from the knowledge base.
- When summarizing experience for a job, pick the subtopics in `knowledge/experience.md` that best match the vacancy and rephrase them in the job's language.
- When a user provides a new fact, ask to save it if persistence is needed, then use `scripts/add_profile_fact.py`.

## Scripts

### `scripts/show_profile.py`

Use this script to print the full knowledge base or selected sections.

Examples:

```bash
python scripts/show_profile.py
python scripts/show_profile.py tech-stack projects
```

Allowed section names: `profile`, `experience`, `tech-stack`, `projects`, `education`, `languages`.

### `scripts/add_profile_fact.py`

Use this script to append a new fact to one section.

Example:

```bash
python scripts/add_profile_fact.py projects "Built a resume AI agent with Microsoft Agent Framework and file-based skills."
```

Allowed section names: `profile`, `experience`, `tech-stack`, `projects`, `education`, `languages`.
