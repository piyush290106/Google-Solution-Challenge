# FairAI – Bias Detection & Fair Decision System

FairAI is an AI-powered prototype for the Hack2Skill Solution Challenge 2026 under the problem statement **[Unbiased AI Decision] Ensuring Fairness and Detecting Bias in Automated Decisions**.

It helps teams upload a CSV dataset, select a sensitive attribute and target outcome, calculate fairness metrics, and generate an AI-assisted explanation using Google Gemini.

## Key Features

- Upload a CSV dataset
- Select sensitive attribute such as gender, income group, caste/category, etc.
- Select target decision column such as hired, approved, shortlisted, selected
- Detect group-wise selection rate
- Calculate demographic parity difference
- Calculate disparate impact ratio
- Show fairness status as Low / Medium / High risk
- Generate recommendations using Google Gemini API when configured
- Fallback rule-based explanation when Gemini API key is not present
- Cloud-ready with Docker and Google Cloud Run deployment support

## Tech Stack

- Python
- Flask
- Pandas
- Scikit-learn
- Google Gemini API
- HTML / CSS / JavaScript
- Docker
- Google Cloud Run

## Folder Structure

```text
FairAI_Full_Project/
├── app.py
├── bias_engine.py
├── requirements.txt
├── Dockerfile
├── cloudbuild.yaml
├── .env.example
├── data/
│   └── sample_hiring_bias.csv
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── docs/
│   ├── Demo_Script.md
│   ├── PPT_Content.md
│   └── screenshots/
└── deployment/
    └── cloud-run-deploy.md
```

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:8080`

## Optional Gemini Setup

Create a `.env` file or set this environment variable:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

FairAI uses Gemini for natural-language bias explanations and recommendations. If no API key is configured, the app still works with a built-in explanation engine.

## Demo Flow

1. Open the web app.
2. Upload `data/sample_hiring_bias.csv`.
3. Choose sensitive attribute: `gender`.
4. Choose target column: `hired`.
5. Click **Analyze Fairness**.
6. Show fairness metrics, risk score, and AI recommendation.

## Submission Links to Add Later

- GitHub Public Repository: Add your GitHub repo link
- Demo Video Link: Add YouTube/Drive 3-minute demo video link
- MVP Link: Add deployed Cloud Run or Render link
- Working Prototype Link: Add deployed app link

## Important

This project is a working prototype. For production usage, sensitive attributes must be handled carefully with privacy, consent, and governance checks.
