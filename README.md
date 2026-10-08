# AI Text & Sentiment Analyzer

A Flask web app that analyzes sentiment and summarizes text using Hugging Face inference APIs.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`.

## Hugging Face API key

Set `HF_API_KEY` in the environment to authenticate inference requests. Keep the token private; do not commit it to this repository. The app can start without a token, but inference requests may be rejected by the model API.

## Deploy to Render

This repository includes `render.yaml` for a Render web service. Create a new Blueprint from this repository in Render. After deployment, set `HF_API_KEY` in the service environment variables for authenticated inference. Render will provide the public service URL.

The start command uses Gunicorn and listens on the port provided by the hosting platform.
