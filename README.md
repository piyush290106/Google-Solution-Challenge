# FairAI – AI-Powered Bias Detection & Fair Decision System

FairAI is an AI-powered prototype developed for the Hack2Skill Solution Challenge 2026 under the problem statement:

**Unbiased AI Decision – Ensuring Fairness and Detecting Bias in Automated Decisions**

It enables users to upload datasets, analyze fairness across sensitive groups, and generate AI-assisted explanations using Google Gemini.

---

## 🚀 Key Features

- Upload a CSV dataset  
- Select sensitive attribute (e.g., gender, income group, caste/category)  
- Select target decision column (e.g., hired, approved, shortlisted)  
- Compute group-wise selection rates  
- Calculate **Demographic Parity Difference**  
- Calculate **Disparate Impact Ratio**  
- Display fairness risk level (Low / Medium / High)  
- Generate AI-powered explanations using Google Gemini  
- Fallback rule-based explanation if API key is not provided  
- Cloud-ready deployment using Docker and Render / Cloud Run  

---

## 🛠️ Tech Stack

- Python  
- Flask  
- Pandas  
- Scikit-learn  
- Google Gemini API  
- HTML / CSS / JavaScript  
- Docker  
- Google Cloud Run / Render  

---

## 📁 Folder Structure

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

---

## ▶️ Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python app.py
```

Open in browser:  
👉 http://127.0.0.1:8080

---

## 🔐 Optional Gemini Setup

Create a `.env` file or set this environment variable:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

FairAI uses Gemini for natural-language explanations and recommendations.  
If no API key is configured, the system uses a built-in rule-based explanation engine.

---

## 🎬 Demo Flow

1. Open the deployed web app  
2. Upload `data/sample_hiring_bias.csv`  
3. Select sensitive attribute: **gender**  
4. Select target column: **hired**  
5. Click **Analyze Fairness**  
6. View fairness metrics, risk level, and AI-generated insights  

---

## 🔗 Submission Links

- **GitHub Repository:**  
  https://github.com/piyush290106/Google-Solution-Challenge  

- **Demo Video (3 mins):**  
  https://drive.google.com/file/d/1PidqsSXiI9mMikn_8vrDdKj4Iw3cUp1U/view  

- **MVP (Live App):**  
  https://google-solution-challenge-2a2i.onrender.com  

- **Working Prototype:**  
  Same as MVP (fully deployed)

---

## 🚀 Impact

FairAI helps organizations:

- Detect bias in automated decision systems  
- Promote fair and transparent AI practices  
- Support ethical hiring, lending, and selection processes  
- Build trust in AI-driven decision-making  

---

## ⚠️ Disclaimer

FairAI is a prototype developed for demonstration purposes.  
In real-world applications, handling sensitive attributes requires strict adherence to privacy, consent, and ethical governance standards.

---


