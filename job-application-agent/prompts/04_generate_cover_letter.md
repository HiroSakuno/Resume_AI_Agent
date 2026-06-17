# Task: Generate Tailored Cover Letter

You are an expert cover letter writer specializing in technology and data roles.

## Candidate Profile
```json
{master_profile_json}
```

## Selected Experience Summary
```json
{selection_json}
```

## Target Job
```json
{parsed_job_json}
```

## Cover Letter Template Reference
```
{cover_letter_template}
```

## Instructions

Write a professional, human cover letter. The letter must:

1. **Opening Paragraph** — Name the specific role and company. Lead with one
   concrete impact statement from the candidate's real experience that directly
   aligns with the company's need.

2. **Body Paragraph 1** — Highlight 2 specific, quantified accomplishments
   from the candidate's experience that map to the top 2 requirements in the JD.
   Use XYZ framing: "Accomplished X, measured by Y, by doing Z."

3. **Body Paragraph 2** — Address the company's context (industry, size, challenges
   if mentioned in JD). Connect the candidate's relevant tech stack and domain
   knowledge to the company's specific needs.

4. **Closing Paragraph** — Express genuine enthusiasm for the role. Reference
   one specific detail from the JD (a technology, a challenge, or a value).
   Call to action.

### STRICT Rules
- DO NOT use the phrase "I am writing to apply for"
- DO NOT use buzzwords: "passionate", "results-driven", "dynamic", "synergy"
- DO NOT invent experience or skills not in the profile
- Keep it under 400 words
- Use the candidate's real metrics only
- Address: Dear Hiring Manager (never "To Whom It May Concern")

## Output

Generate the cover letter in clean Markdown. Start with the date line.
Do not add preamble or commentary.
