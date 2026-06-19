# Resume-AI-Agent

A Microsoft Foundry hosted agent built with Agent Framework.

## Quick Start

### Prerequisites
- Python 3.10+
- Azure Developer CLI (`azd`) or VS Code Foundry Toolkit
- Azure subscription with Foundry project

### Run Locally
```bash
python main.py
```

The agent will start on `http://localhost:8088`.

### Deploy to Foundry
1. Open Command Palette (`Cmd+Shift+P`)
2. Run **Foundry Toolkit: Deploy Hosted Agent**
3. Follow the deployment wizard

## Adding Skills

Create a new skill folder in `skills/`:
```
skills/my-skill/
├── SKILL.md
└── scripts/
    └── my_script.py
```

Skills are discovered automatically and available to the agent.

## Personal Profile Knowledge

The agent includes a `personal-profile` skill for resume and career knowledge:

```text
skills/personal-profile/
├── SKILL.md
├── knowledge/
│   ├── education.md
│   ├── experience.md
│   ├── languages.md
│   ├── profile.md
│   ├── projects.md
│   └── tech-stack.md
└── scripts/
    ├── add_profile_fact.py
    └── show_profile.py
```

Fill the `TODO` items in `skills/personal-profile/knowledge/` with your real background. The agent is instructed to use this skill for resume, interview, portfolio, and career-story questions, and to avoid inventing missing personal facts.
