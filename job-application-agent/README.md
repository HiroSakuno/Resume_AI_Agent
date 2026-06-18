# AI Job Application Generator

A local Python-based AI agent that generates tailored resumes, cover letters,
and ATS reports for job applications using Claude (claude-sonnet-4-6).

## Folder Structure

```
job-application-agent/
├── profile/               # Your personal YAML profile data
├── templates/             # Output format templates
├── job_descriptions/
│   ├── raw/               # Paste raw .txt job descriptions here
│   └── parsed/            # Auto-saved parsed JSON
├── outputs/               # Generated applications (dated folders)
├── prompts/               # 6-step Claude prompts
├── scripts/
│   ├── generate_application.py  # Main entry point
│   ├── export_docx.py
│   └── export_pdf.py
├── .env                   # Your API key (never commit this)
├── .env.example
└── requirements.txt
```

## Setup

### 1. Install Dependencies

```bash
cd "/Users/hiro/Library/CloudStorage/OneDrive-Personal/Work/Resume Agent/job-application-agent"
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set API Key

```bash
cp .env.example .env
# Edit .env and paste your Anthropic API key
```

### 3. Update Your Profile

Edit the YAML files in `profile/` with your real information:
- `master_profile.yaml` — name, contact, summary
- `experience.yaml` — work history with achievements
- `skills.yaml` — your skill categories
- `certifications.yaml` — your certifications
- `education.yaml` — your education
- `achievements.yaml` — key accomplishments with metrics
- `projects.yaml` — personal or professional projects to use when relevant

## Usage

### Option 1: From a .txt file

Save the job description as a plain text file:

```bash
python scripts/generate_application.py --job job_descriptions/raw/job_001.txt
```

### Option 2: Paste directly

```bash
python scripts/generate_application.py --job-text "Senior BI Engineer at Acme Corp..."
```

### Skip export (faster, .md only)

```bash
python scripts/generate_application.py --job job_descriptions/raw/job.txt --no-export
```

## Output

Each run creates a folder: `outputs/CompanyName_RoleName_YYYY-MM-DD/`

Contents:
- `resume.md` / `.docx` / `.pdf`
- `cover_letter.md` / `.docx` / `.pdf`
- `ats_report.md`
- `quality_check.md`
- `parsed_job.json`
- `selection_strategy.json`

## Notes

- The agent **never invents experience** — it only uses data from your YAML profile.
- All bullet points follow the XYZ format: "Accomplished X, measured by Y, by doing Z."
- Resumes are ATS-friendly: no tables, columns, images, or special characters.
- Estimated cost per run: ~$0.05–$0.15 using claude-sonnet-4-6.
