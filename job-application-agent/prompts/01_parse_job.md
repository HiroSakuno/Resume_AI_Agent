# Task: Parse Job Description

You are a job description analyst. Your task is to extract structured information
from the raw job description below.

## Job Description (Raw Input)

```
{job_description_text}
```

## Instructions

Extract and return a JSON object with EXACTLY the following structure. Do not
add extra keys. If a field cannot be determined, use null or an empty array.

```json
{{
  "company_name": "string — name of the hiring company",
  "role_title": "string — exact job title",
  "role_level": "string — one of: junior, mid, senior, lead, principal, staff, manager, director",
  "employment_type": "string — one of: full-time, part-time, contract, freelance",
  "location": "string — location or 'Remote'",
  "remote_ok": true,
  "salary_range": "string or null",
  "tech_stack": ["array of specific technologies, tools, platforms mentioned"],
  "required_skills": ["array of explicitly required skills"],
  "preferred_skills": ["array of nice-to-have skills"],
  "responsibilities": ["array of key job responsibilities"],
  "qualifications": ["array of required qualifications"],
  "industry": "string — e.g. Technology, Finance, CPG, Healthcare",
  "ats_keywords": ["array of high-frequency keywords likely used by ATS systems"],
  "company_values": ["array of culture or values signals if present"]
}}
```

Return ONLY the JSON. No explanation, no markdown code fence.
