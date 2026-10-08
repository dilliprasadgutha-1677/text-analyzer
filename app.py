import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests

SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
SUMMARIZE_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

# Retrieve API key from environment variable
HF_API_KEY = os.getenv("HF_API_KEY", "")
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

def query_hf(api_url, payload):
    try:
        response = requests.post(api_url, headers=HEADERS, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Hugging Face API Error: {e}")
        return {"error": str(e)}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Empty text provided"}), 400

    # Call Sentiment API
    sentiment_res = query_hf(SENTIMENT_API_URL, {"inputs": text})
    # Call Summarization API
    summary_res = query_hf(SUMMARIZE_API_URL, {"inputs": text, "parameters": {"max_length": 100, "min_length": 30}})

    # Process Sentiment Response
    sentiment_label = "UNKNOWN"
    sentiment_score = 0.0
    
    if isinstance(sentiment_res, list) and len(sentiment_res) > 0:
        top_res = sentiment_res[0][0] if isinstance(sentiment_res[0], list) else sentiment_res[0]
        sentiment_label = top_res.get("label", "UNKNOWN")
        sentiment_score = round(top_res.get("score", 0.0) * 100, 2)
    elif isinstance(sentiment_res, dict) and "error" in sentiment_res:
        sentiment_label = "API Error"

    # Process Summary Response
    summary_text = "Could not generate summary."
    if isinstance(summary_res, list) and len(summary_res) > 0:
        summary_text = summary_res[0].get("summary_text", summary_text)
    elif isinstance(summary_res, dict) and "error" in summary_res:
        summary_text = f"API Error: {summary_res['error']}"

    return jsonify({
        "sentiment": sentiment_label,
        "confidence": f"{sentiment_score}%",
        "summary": summary_text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
