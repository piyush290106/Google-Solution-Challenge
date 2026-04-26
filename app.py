from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import uuid
from dotenv import load_dotenv
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


SENSITIVE_KEYWORDS = [
    "gender", "sex", "age", "caste", "race", "religion",
    "income", "category", "community", "region", "location",
    "disability", "ethnicity", "marital"
]

TARGET_KEYWORDS = [
    "hired", "selected", "approved", "admitted", "accepted",
    "decision", "status", "result", "loan_status", "target",
    "outcome", "eligible", "passed"
]

POSITIVE_WORDS = [
    "1", "yes", "true", "approved", "selected", "hired",
    "accepted", "admitted", "eligible", "pass", "passed"
]


def detect_sensitive_column(df):
    columns = list(df.columns)

    for col in columns:
        lower = col.lower()
        for key in SENSITIVE_KEYWORDS:
            if key in lower:
                return col

    categorical_cols = []

    for col in columns:
        unique_count = df[col].nunique()
        if unique_count >= 2 and unique_count <= 10:
            categorical_cols.append(col)

    if categorical_cols:
        return categorical_cols[0]

    return columns[0]


def detect_target_column(df, sensitive_col):
    columns = [col for col in df.columns if col != sensitive_col]

    for col in columns:
        lower = col.lower()
        for key in TARGET_KEYWORDS:
            if key in lower:
                return col

    binary_cols = []

    for col in columns:
        unique_values = df[col].dropna().astype(str).str.lower().unique()
        if len(unique_values) == 2:
            binary_cols.append(col)

    if binary_cols:
        return binary_cols[0]

    return columns[-1]


def detect_positive_label(df, target_col):
    values = df[target_col].dropna().astype(str).str.lower().unique()

    for word in POSITIVE_WORDS:
        if word in values:
            original_value = df[target_col].dropna().astype(str).unique()
            for val in original_value:
                if val.lower() == word:
                    return val

    numeric_values = pd.to_numeric(df[target_col], errors="coerce")

    if numeric_values.notna().all():
        return str(numeric_values.max())

    return df[target_col].dropna().astype(str).unique()[0]


def calculate_selection_rates(df, sensitive_col, target_col, positive_label):
    rates = {}

    groups = df[sensitive_col].dropna().unique()

    for group in groups:
        group_data = df[df[sensitive_col] == group]
        selected = group_data[group_data[target_col].astype(str) == str(positive_label)]

        if len(group_data) == 0:
            rates[str(group)] = 0
        else:
            rates[str(group)] = round(len(selected) / len(group_data), 3)

    return rates


def calculate_fairness_metrics(rates):
    values = list(rates.values())

    if not values:
        return 0, 0, "Low", 100

    max_rate = max(values)
    min_rate = min(values)

    dp_diff = round(max_rate - min_rate, 3)

    if max_rate == 0:
        dir_ratio = 0
    else:
        dir_ratio = round(min_rate / max_rate, 3)

    fairness_score = round(max(0, 1 - dp_diff) * 100, 2)

    if dp_diff >= 0.5 or dir_ratio < 0.5:
        risk = "High"
    elif dp_diff >= 0.25 or dir_ratio < 0.8:
        risk = "Medium"
    else:
        risk = "Low"

    return dp_diff, dir_ratio, risk, fairness_score


def generate_mitigated_rates(before_rates):
    avg_rate = round(sum(before_rates.values()) / len(before_rates), 3)

    after_rates = {}

    for group in before_rates:
        after_rates[group] = avg_rate

    return after_rates


def generate_ai_explanation(
    sensitive_col,
    target_col,
    positive_label,
    before_rates,
    after_rates,
    dp_diff,
    dir_ratio,
    risk,
    fairness_score
):
    fallback = f"""
FairAI automatically detected "{sensitive_col}" as the sensitive attribute and "{target_col}" as the target decision column.

The positive decision label is "{positive_label}".

The system detected a {risk.lower()} bias risk.
The demographic parity difference is {dp_diff}, and the disparate impact ratio is {dir_ratio}.
The fairness score is {fairness_score}%.

Before mitigation, selection rates were:
{before_rates}

After suggested mitigation, fair selection rates become:
{after_rates}

Recommended actions:
1. Balance under-represented groups in the dataset.
2. Review whether the sensitive attribute affects the decision.
3. Use fairness-aware model evaluation.
4. Add human review for high-impact decisions.
"""

    if not GOOGLE_API_KEY:
        return fallback

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an AI fairness expert.

FairAI automatically analyzed this dataset.

Sensitive attribute: {sensitive_col}
Target decision column: {target_col}
Positive label: {positive_label}

Before mitigation rates:
{before_rates}

Suggested fair rates:
{after_rates}

Demographic parity difference: {dp_diff}
Disparate impact ratio: {dir_ratio}
Risk level: {risk}
Fairness score: {fairness_score}%

Explain:
1. What bias is present
2. Why it matters
3. What mitigation means
4. Recommendations
5. Real-world use cases

Keep it professional and suitable for hackathon judges.
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return fallback


def create_pdf_report(path, result):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - inch

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "FairAI - Automated Bias Detection Report")

    y -= 40
    c.setFont("Helvetica", 11)

    lines = [
        f"Rows analyzed: {result['rows']}",
        f"Auto-detected sensitive attribute: {result['sensitive_col']}",
        f"Auto-detected target column: {result['target_col']}",
        f"Auto-detected positive label: {result['positive_label']}",
        f"Risk level: {result['risk_level']}",
        f"Fairness score: {result['fairness_score']}%",
        f"Demographic parity difference: {result['dp_diff']}",
        f"Disparate impact ratio: {result['dir_ratio']}",
        "",
        f"Before mitigation: {result['before_rates']}",
        f"After mitigation: {result['after_rates']}",
        "",
        "AI Explanation:",
    ]

    for line in lines:
        c.drawString(50, y, line[:100])
        y -= 20

    explanation_lines = result["ai_explanation"].split("\n")

    for line in explanation_lines:
        if y < 70:
            c.showPage()
            y = height - inch
            c.setFont("Helvetica", 10)

        c.drawString(50, y, line[:100])
        y -= 15

    c.save()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    report_file = None

    if request.method == "POST":
        file = request.files.get("csv_file")

        if not file or not file.filename.endswith(".csv"):
            return render_template(
                "index.html",
                result=None,
                report_file=None,
                error="Please upload a valid CSV file."
            )

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        df = pd.read_csv(file_path)

        sensitive_col = detect_sensitive_column(df)
        target_col = detect_target_column(df, sensitive_col)
        positive_label = detect_positive_label(df, target_col)

        before_rates = calculate_selection_rates(
            df,
            sensitive_col,
            target_col,
            positive_label
        )

        dp_diff, dir_ratio, risk, fairness_score = calculate_fairness_metrics(before_rates)

        after_rates = generate_mitigated_rates(before_rates)

        after_dp_diff, after_dir_ratio, after_risk, after_fairness_score = calculate_fairness_metrics(after_rates)

        ai_explanation = generate_ai_explanation(
            sensitive_col,
            target_col,
            positive_label,
            before_rates,
            after_rates,
            dp_diff,
            dir_ratio,
            risk,
            fairness_score
        )

        result = {
            "rows": len(df),
            "sensitive_col": sensitive_col,
            "target_col": target_col,
            "positive_label": positive_label,
            "before_rates": before_rates,
            "after_rates": after_rates,
            "dp_diff": dp_diff,
            "dir_ratio": dir_ratio,
            "risk_level": risk,
            "fairness_score": fairness_score,
            "after_dp_diff": after_dp_diff,
            "after_dir_ratio": after_dir_ratio,
            "after_risk_level": after_risk,
            "after_fairness_score": after_fairness_score,
            "ai_explanation": ai_explanation
        }

        report_file = f"fairai_report_{uuid.uuid4().hex[:8]}.pdf"
        report_path = os.path.join(REPORT_FOLDER, report_file)

        create_pdf_report(report_path, result)

    return render_template(
        "index.html",
        result=result,
        report_file=report_file
    )


@app.route("/download/<filename>")
def download_report(filename):
    path = os.path.join(REPORT_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
        app.run(debug=True)