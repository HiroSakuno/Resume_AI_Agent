# Resume Generation Rules

## Core Principles

* Never invent companies, job titles, projects, achievements, metrics, certifications, technologies, or responsibilities.
* Only use information explicitly available in:

  * `experience.json`
  * `projects.json`
* Adapt wording and emphasis to the target job description while preserving factual accuracy.
* Optimize for ATS (Applicant Tracking Systems) using clear, concise, and technical language.
* Prioritize measurable impact and business outcomes whenever available.

## Skill Usage Rules

* Only mention skills, tools, platforms, frameworks, certifications, or technologies that exist in the candidate profile.
* Do not add technologies simply because they appear in the job description.
* If a technology is requested but not present in the candidate profile:

  * Do not claim professional experience.
  * Reposition it as:
    * Exposure
    * Self-study
    * Personal project
    * Hands-on project
    * Certification preparation
  * Only if supported by available profile data.

## Experience Selection Rules

* Experience content is pre-defined in the experience database.
* Do not create new responsibilities, achievements, projects, metrics, or technologies.
* Do not rewrite experience beyond minor grammatical or ATS-oriented adjustments.
* Select the most relevant experiences, achievements, and projects based on the target job description.
* Prioritize experiences that demonstrate direct alignment with the required skills, technologies, and business domain.
* Preserve all factual information exactly as stored in the source data.
* When multiple achievements exist for the same role, select the ones that best match the job requirements.
* Prefer measurable achievements when available.
* Maintain chronological consistency and original employment history.

### Selection Priorities

For AI Engineer / AI Automation roles, prioritize experience containing:

* Python
* SQL
* AI Agents
* LLM Applications
* RAG
* Workflow Automation
* API Integrations
* Cloud Platforms
* Microsoft Foundry / Azure AI Foundry
* n8n
* Agent Orchestration
* Data Pipelines

For BI / Analytics roles, prioritize experience containing:

* Power BI
* DAX
* SQL
* Data Modeling
* ETL / ELT
* Databricks
* Azure
* Dashboard Development
* Semantic Models
* Performance Optimization
* RLS / OLS
* Stakeholder Management

### Truthfulness Rule

The resume generator must only assemble and prioritize existing experience content. It must never generate new experience content that is not present in the approved candidate profile.

## ATS Optimization Rules

* Mirror relevant terminology from the job description when supported by the candidate profile.
* Use standard industry terminology.
* Avoid excessive buzzwords.
* Avoid graphics, tables, icons, emojis, and ATS-unfriendly formatting.
* Ensure important keywords appear naturally within experience descriptions, skills, and summary sections.

## Truthfulness Rule

The generated resume must always remain truthful, defensible during interviews, and fully aligned with the candidate's real experience and documented projects.