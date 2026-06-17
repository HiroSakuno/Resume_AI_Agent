# Task: ATS Keyword Match Analysis

You are an ATS (Applicant Tracking System) specialist. Analyze the generated
resume against the job description for keyword optimization.

## Generated Resume
```
{generated_resume}
```

## Parsed Job Description
```json
{parsed_job_json}
```

## ATS Review Template
```
{ats_review_template}
```

## Instructions

Perform a rigorous ATS analysis:

1. **Match Score**: Estimate keyword match percentage (0-100). Count how many
   of the JD's required skills and keywords appear in the resume.

2. **Keywords Found**: List keywords from the JD that ARE present in the resume.
   Group by: Technical Skills | Soft Skills | Industry Terms

3. **Missing Keywords — High Priority**: Skills or terms explicitly marked
   "required" or appearing 3+ times in the JD that are ABSENT from the resume.

4. **Missing Keywords — Medium Priority**: Skills listed as "preferred" or
   appearing once that are absent.

5. **Recommendations**: Specific, actionable edits to improve ATS score.
   For each missing high-priority keyword, suggest WHERE in the resume it
   could be naturally added (if the candidate actually has that skill).

6. **Formatting Checklist**: Verify the resume passes these ATS rules:
   - [ ] Standard section headings used (no creative names)
   - [ ] No tables or columns
   - [ ] No images or graphics
   - [ ] Clean bullet points
   - [ ] Contact info at top
   - [ ] Date formats consistent
   - [ ] File-safe characters only

## Output

Generate the ATS report in clean Markdown using the template structure.
Include exact keyword counts where possible. Do not add preamble.
