# 3-Minute Demo Script – FairAI

## 0:00–0:20 Problem
Automated AI decisions are increasingly used in hiring, lending, education, and public services. If these systems are trained on biased data, they can create unfair outcomes for specific groups.

## 0:20–0:50 Solution
FairAI is a bias detection and fairness audit platform. It allows a user to upload a dataset, choose a sensitive attribute and decision column, and instantly understand whether the decision pattern is fair.

## 0:50–2:10 Demo
1. Open FairAI web app.
2. Upload sample_hiring_bias.csv.
3. Select gender as the sensitive attribute.
4. Select hired as the decision column.
5. Click Analyze Fairness.
6. Show risk level, demographic parity difference, disparate impact ratio, and group-wise selection chart.
7. Show Gemini-generated explanation and recommendations.

## 2:10–2:40 Technology
FairAI uses Python, Flask, Pandas, fairness metrics, and Google Gemini API. It can be deployed on Google Cloud Run for scalable access.

## 2:40–3:00 Future Scope
Future improvements include automatic data repair, fairness-aware model training, enterprise dashboards, and integration with HR, lending, and admission systems.
