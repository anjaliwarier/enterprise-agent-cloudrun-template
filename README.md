# ADK Agent Cloud Run Deployment Demo

This demo showcases the native enterprise features of the **Gemini Enterprise Agent Platform** with the **Agent Development Kit (ADK)**:
1. Exposing an ADK Agent via FastAPI.
2. Deploying the FastAPI app to **Google Cloud Run**.
3. Natively streaming telemetry for **Observability & Tracing** directly into Cloud Trace and Vertex AI Observability.
4. Running native programmatic **Evaluations** using `google.adk.evaluation`.

---

## 📁 Directory Structure

```bash
adk-cloudrun-demo/
├── agent.py            # ADK LlmAgent with tools
├── main.py             # FastAPI server exposing /invoke
├── requirements.txt    # App dependencies
├── Dockerfile          # Optimized Cloud Run container
├── deploy.sh           # Shell script for Cloud Build & Cloud Run
├── eval_suite.py       # Async programmatic Evaluation suite
└── eval_data/
    └── eval_set.json   # Mock evaluation dataset
```

---

## 🛠️ Pre-requisites & Configuration

Before running or deploying this demo, configure your Google Cloud parameters in a single `.env` file:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your actual **GCP Project ID**, preferred **Location**, and your **GCS Staging Bucket name**. The scripts (`deploy.sh`, `register_agent.py`, and `eval_suite.py`) will dynamically load all parameters from this single file!

Ensure you have the Google Cloud CLI installed and setup:
- Set active project in `gcloud`:
  ```bash
  gcloud config set project YOUR_GCP_PROJECT_ID
  ```
- Enable necessary Google Cloud APIs:
  ```bash
  gcloud services enable run.googleapis.com cloudbuild.googleapis.com cloudtrace.googleapis.com aiplatform.googleapis.com artifactregistry.googleapis.com
  ```

---

## 🚀 1. Local Development & Testing

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run FastAPI Server Locally
```bash
export GOOGLE_CLOUD_PROJECT="YOUR_GCP_PROJECT_ID"
python main.py
```
The app runs at `http://localhost:8080`.

### Test endpoint
```bash
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is property insurance operational risk?"}'
```

---

## 🌍 2. Automate Deployment to Cloud Run

Deploy seamlessly to Cloud Run using the provided automation script:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 👁️ 3. Native Gemini Enterprise Observability

By deploying with ADK and modern gen-ai integrations, Observability & Tracing are streams powered out-of-the-box:
- **Traces**: Every tool call (e.g., `google_search`), model invocation, and prompt latency is automatically captured.
- **Viewing Traces**:
  1. Navigate to the **Google Cloud Console**.
  2. Search for **Cloud Trace**.
  3. Explore the timeline to see agent execution latency and breakdown step-by-step!

---

## 🧪 4. Native Gemini Enterprise Programmatic Evaluations

Run the evaluation suite programmatically against your agent:
```bash
export GOOGLE_CLOUD_PROJECT="YOUR_GCP_PROJECT_ID"
python eval_suite.py
```
The results, metric scoring, and evaluation details will natively stream and populate directly inside the **Vertex AI Evaluation** UI in the Google Cloud Console.
