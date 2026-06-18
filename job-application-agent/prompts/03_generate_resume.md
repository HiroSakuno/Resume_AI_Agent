# Resume Generation Rules

## Objective

Generate a highly ATS-optimized resume tailored to a specific job description using the provided candidate data.

The generated resume must:

* Never invent technologies, projects, certifications, responsibilities, or achievements.
* Emphasize experiences and skills most relevant to the target job.
* Follow the exact structure defined below.
* Use concise, recruiter-friendly language.
* Be optimized for ATS parsing and keyword matching.

---

# Input Variables

## Candidate Master Profile
json
{master_profile_json}
## Selected Experience and Strategy
json
{selection_json}
## Full Experience Data (for selected IDs only)
json
{selected_experience_json}
## Selected Projects Data
json
{selected_projects_json}
## Target Job
json
{parsed_job_json}
## Templates Reference
{resume_template}

---

# Global Writing Rules

## Rule 1 — Never Invent

Do not invent:

* Technologies
* Certifications
* Responsibilities
* Metrics
* Projects
* Years of experience
* Leadership experience

Everything must come from the provided data.

---

## Rule 2 — ATS Optimization

Prioritize exact terminology used in the job description.

Example:

If the JD says:

* Python
* REST APIs
* LLMs
* Workflow Automation

Then those exact terms should appear naturally throughout the resume when supported by the candidate's experience.

---

## Rule 3 — Professional Summary

Length:

2 paragraphs.

Structure:

Paragraph 1:

* Current professional identity.
* Years of experience.
* Core expertise.
* Positioning toward the target role (if Relevant)


Paragraph 2:

* Business impact.
* International experience.
* Stakeholder collaboration.

Use:

* hands-on experience
* practical experience
* personal projects

when appropriate.

---

## Rule 4 — Experience Selection

Only include:

* Selected experiences from selection_json.

Maximum:

* professional experiences.

Order:

Most recent first.

---

## Rule 5 — Experience Format

Every experience must follow this exact format:

```text
### Job Title

Company — Employment Type, Location
Date Range - sum of time

Context paragraph.

- Achievement or responsibility
- Achievement or responsibility
- Achievement or responsibility
- Achievement or responsibility

Tech Stack: ...
```

---

## Rule 7 — Bullet Rules

Use exactly 4–5 bullets.

Each bullet must:

* Start with an action verb.
* Be outcome-focused.
* Explain business value.

Preferred verbs:

* Built
* Developed
* Designed
* Optimized
* Automated
* Implemented
* Reduced
* Improved
* Supported
* Collaborated
* Created
* Delivered

try to mention the important stack that the job require

---

## Rule 8 — Metrics

Always preserve existing metrics.

Examples:

Good:

```text
Reduced Power BI capacity consumption by approximately 50%.
```

```text
Built reporting solutions used across 3,600 schools.
```

Bad:

```text
Reduced costs significantly.
```

Never create metrics.

---

# AI Project Section Rules

Include this section only if:

* Selected Projects Data is not empty.
* The projects are related to the position.

```text
SELECTED  PROJECTS
```

---

## Project Format

```text
### Project Name

Project Type

Project summary.

- Bullet
- Bullet
- Bullet

Tech Stack: ...
```

Use only projects from Selected Projects Data. Do not invent projects,
project years, technologies, or outcomes.

---

## AI Transition Rule

If the target role is:

* AI Engineer
* AI Automation Engineer
* AI Agent Developer
* LLM Engineer

and the candidate is transitioning from another field:

Position as:

```text
Transitioning into AI Engineering
```

or

```text
Transitioning into AI Automation Engineering
```

Never position as:

```text
Senior AI Engineer
```

unless professional experience explicitly exists.

---

# Core Skills Rules

Create sections:

```text
AI & Automation

Programming & Technical Execution

Data & Analytics Engineering

Databases & Cloud Platforms

Business & Collaboration
```

Only include categories relevant to the job.

Order categories by relevance to the target role.

---

# Certifications

Format:

```text
## CERTIFICATIONS

Certification Name
Issuer
```

Example:

```text
Microsoft Certified: Power BI Data Analyst Associate (PL-300)
Microsoft
```

---

# Education

Format:

```text
## EDUCATION

Degree Name
Institution
Location
```

---

# Languages

Format:

```text
## LANGUAGES

Portuguese: Native

English: Advanced / Professional working proficiency
```

---

# Resume Tailoring Logic

Before generating the resume:

1. Analyze the target role.
2. Identify top required skills.
3. Rank candidate experiences by relevance.
4. Reorder emphasis inside the experience bullets.
5. Reorder skills section.
6. Highlight matching technologies.
7. Highlight matching projects.
8. Highlight matching certifications.

---

# Output Requirements

Output valid Markdown only.

Do not explain decisions.

Do not include notes.

Do not include reasoning.

Do not include ATS score.

Do not include comments.

Return only the final resume.
