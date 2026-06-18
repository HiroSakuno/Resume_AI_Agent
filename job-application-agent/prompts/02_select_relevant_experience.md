# Task: Select and Rank Relevant Experience

You are a resume strategist. Your task is to review the candidate's full profile
and select the most relevant experience, achievements, and skills for the target role.

## Candidate Profile

### Work Experience
```json
{experience_json}
```

### Projects
```json
{projects_json}
```

### All Skills
```json
{skills_json}
```

### All Achievements
```json
{achievements_json}
```

### Certifications
```json
{certifications_json}
```

## Target Job (Parsed)
```json
{parsed_job_json}
```

## Instructions

1. Select the TOP 2-3 experience entries most relevant to this role.
2. For each selected experience, identify the 2-3 strongest achievements to highlight.
3. Select up to 2 projects only when they are relevant to the target role.
4. Select the most relevant skills clusters (max 5 categories).
5. Flag any skill GAPS — skills the JD requires that the candidate does not have.
6. Identify keywords from the JD to naturally embed in the resume.

Return a JSON object with this EXACT structure:

```json
{{
  "selected_experience_ids": ["exp_001", "exp_002"],
  "selected_project_ids": ["proj_001"],
  "achievement_map": {{
    "exp_001": ["achievement text 1", "achievement text 2"],
    "exp_002": ["achievement text 1"]
  }},
  "selected_skill_clusters": ["bi_and_analytics", "data_engineering"],
  "skill_gaps": ["string — skills in JD not in candidate profile"],
  "keywords_to_embed": ["list of high-priority ATS keywords to use naturally"],
  "positioning_angle": "string — one paragraph describing how to frame this candidate for this role"
}}
```

Return ONLY the JSON. No explanation, no markdown code fence.
