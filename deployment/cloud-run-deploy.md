# Deploy FairAI on Google Cloud Run

## 1. Enable APIs

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## 2. Set your project

```bash
gcloud config set project YOUR_PROJECT_ID
```

## 3. Add Gemini API key as a secret/environment variable

```bash
gcloud run deploy fairai \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

## 4. Alternative with Cloud Build

```bash
gcloud builds submit --config cloudbuild.yaml
```

## 5. Submission

Copy the Cloud Run service URL and paste it as the MVP/Working Prototype link in the Hack2Skill form.
