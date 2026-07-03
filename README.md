# AI Task Automation System

A Streamlit workflow assistant that uses the Groq API to summarize emails, classify priority and category, extract actions and deadlines, and draft editable replies. It also processes a CSV batch of emails.

## Features

- Single-email analysis and reply drafting
- Priority, category, deadline, and action extraction
- Configurable reply tone
- CSV batch processing and result download
- API key loaded from the environment or a local `.env` file

## Setup

```powershell
cd ai-task-automation-system
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your key to `.env`:

```text
GROQ_API_KEY=gsk_your_key_here
```

Run:

```powershell
streamlit run app.py
```

## Run with uv

Install `uv`, then from this project directory run:

```powershell
uv venv
uv pip install -r requirements.txt
Copy-Item .env.example .env
uv run streamlit run app.py
```

Alternatively, provide the key only for the current PowerShell session:

```powershell
$env:GROQ_API_KEY="gsk_your_key_here"
uv run streamlit run app.py
```

For batch mode, upload a CSV containing an `email` column. Review every generated reply before sending; this project does not send email automatically.
