# Task: Final Quality Check

You are a senior hiring manager and executive recruiter reviewing a complete
job application package. Perform a final quality check.

## Resume
```
{generated_resume}
```

## Cover Letter
```
{generated_cover_letter}
```

## Target Job
```json
{parsed_job_json}
```

## ATS Report Summary
```
{ats_report_summary}
```

## Instructions

Review the complete application package and provide:

1. **Overall Assessment** (1-2 sentences): Is this application strong for this role?

2. **Resume Score** (1-10): Rate on: ATS compliance, XYZ bullet quality,
   relevance to role, clarity.

3. **Cover Letter Score** (1-10): Rate on: Personalization, specificity,
   tone, call to action.

4. **Top 3 Strengths**: What makes this application stand out.

5. **Top 3 Improvements**: Critical changes that would increase interview rate.
   Be specific (e.g., "Bullet 2 in UT-TECH experience lacks a measurable Y —
   add a specific metric.")

6. **Red Flags** (if any): Anything that might cause an ATS or recruiter
   to reject the application.

7. **Final Recommendation**: One of: SUBMIT_AS_IS | MINOR_REVISIONS | MAJOR_REVISIONS

## Output

Format the output as clean Markdown with the sections above. Be direct,
specific, and constructive. Do not be generic.
