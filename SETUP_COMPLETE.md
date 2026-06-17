# AI Job Application Agent — Setup Complete ✓

## What's Been Created

Your local AI job application agent is fully configured and ready to use. Located at:
```
/Users/hiro/Library/CloudStorage/OneDrive-Personal/Work/Resume Agent/job-application-agent/
```

## Quick Start

### 1. Install Dependencies (One-time)

```bash
cd "/Users/hiro/Library/CloudStorage/OneDrive-Personal/Work/Resume Agent/job-application-agent"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip

python3 -m pip install -r requirements.txt
```

### 2. Add Your API Key

```bash
cp .env.example .env
# Edit .env and paste your Anthropic API key
```

### 3. Run an Application

```bash
# Create a test job description
echo "Senior Power BI Developer at Microsoft..." > job_descriptions/raw/test_job.txt

# Generate application (markdown only, faster)
python scripts/generate_application.py --job job_descriptions/raw/test_job.txt --no-export

# OR with DOCX/PDF export
python scripts/generate_application.py --job job_descriptions/raw/test_job.txt
```

## Project Structure

```
job-application-agent/
├── profile/                    # Your professional data (YAML)
│   ├── master_profile.yaml    # Name, title, summary, contact
│   ├── experience.yaml        # 4 roles with real achievements
│   ├── skills.yaml            # 6 skill clusters (130+ skills)
│   ├── certifications.yaml    # PL-300, DP-203
│   ├── education.yaml         # Education info
│   └── achievements.yaml      # 3 key measurable achievements
│
├── templates/                 # Markdown format templates
│   ├── resume_template.md
│   ├── cover_letter_template.md
│   ├── ats_review_template.md
│   └── linkedin_summary_template.md
│
├── prompts/                   # 6 Claude prompts (chainable)
│   ├── 01_parse_job.md               → job JSON
│   ├── 02_select_relevant_experience.md → selection JSON
│   ├── 03_generate_resume.md          → resume.md (XYZ bullets)
│   ├── 04_generate_cover_letter.md    → cover_letter.md
│   ├── 05_ats_review.md               → ats_report.md
│   └── 06_final_quality_check.md      → quality_check.md
│
├── scripts/
│   ├── generate_application.py  # Main orchestrator
│   ├── export_docx.py           # Markdown → .docx
│   └── export_pdf.py            # Markdown → .pdf
│
├── job_descriptions/
│   ├── raw/                   # Save .txt job descriptions here
│   └── parsed/                # Auto-saved JSON per run
│
├── outputs/                   # Generated applications
│   └── CompanyName_RoleName_YYYY-MM-DD/
│       ├── resume.md / .docx / .pdf
│       ├── cover_letter.md / .docx / .pdf
│       ├── ats_report.md
│       ├── quality_check.md
│       ├── parsed_job.json
│       └── selection_strategy.json
│
├── requirements.txt           # Python dependencies
├── .env.example               # API key template
├── .env                       # Your actual key (create this)
└── README.md                  # Full documentation
```

## Key Features

✓ **Never invents data** — only uses your YAML profile
✓ **XYZ bullet format enforced** — "Accomplished X, measured by Y, by doing Z"
✓ **ATS-optimized** — no tables, no images, clean formatting
✓ **6-step AI pipeline** — modular Claude prompts, parallel-safe
✓ **Multi-format export** — .md, .docx, .pdf all in one run
✓ **Cost-efficient** — ~$0.05–0.15 per application using claude-sonnet-4-6
✓ **Profile-driven** — update YAML once, use for many applications

## Profile Data (Pre-Populated)

Your profile has been populated with:

- **Name:** Hiro Sakuno
- **Title:** Senior BI Engineer / Data Engineer
- **Email:** hirosakuno@gmail.com
- **Portfolio:** https://portfolio.mindthedata.com.br
- **Location:** Brazil (Remote work only)

### Experience (4 roles)
1. AB InBev (Sept 2025–Present) — Senior BI Engineer & BI Architect
2. Sicredi (Sept 2024–Sept 2025) — Senior Power BI Developer
3. Grupo NC (Apr 2023–Sept 2024) — Senior Power BI Developer
4. Dato Tecnologia (Apr 2022–June 2023) — Power BI Developer

### Skills (130+ across 6 categories)
- BI & Analytics (Power BI, DAX, Power Query, Tabular Editor 3, etc.)
- Data Engineering (SQL, Databricks, Azure Data Lake, Airflow, etc.)
- Databases & Sources (Oracle, SQL Server, SAP ECC/S/4HANA, etc.)
- AI & Automation (Azure OpenAI, Semantic Kernel, n8n, etc.)
- SAP & ERP Migration (ECC→S/4HANA, report migration, TMDL, etc.)
- Tools & DevOps (GitHub, Azure DevOps, VS Code, etc.)

### Certifications
- Microsoft PL-300 (Power BI Data Analyst) — 2023

## Next Steps

1. **Test with a real job description:**
   - Copy a job posting into `job_descriptions/raw/test.txt`
   - Run: `python scripts/generate_application.py --job job_descriptions/raw/test.txt`
   - Check the output in `outputs/`

2. **Verify your data:**
   - Edit `profile/experience.yaml` if needed
   - Edit `profile/achievements.yaml` to add/update achievements
   - Keep YAML files in sync with your real background

3. **Customize output:**
   - Tweak prompts in `prompts/` directory if needed
   - Modify templates in `templates/` for different styling

4. **Use multiple times:**
   - Each run creates a new dated folder
   - Compare outputs across multiple job applications
   - Iterate and improve based on quality_check.md feedback

## Estimated Cost

- **Per application:** ~$0.05–$0.15 USD (using claude-sonnet-4-6)
- **With 20 applications:** ~$1–3 total

## Support

- See `README.md` for full CLI documentation
- Each prompt file includes detailed instructions
- `quality_check.md` output provides specific feedback for improvement

---

**Ready to generate your first application!** 🚀
