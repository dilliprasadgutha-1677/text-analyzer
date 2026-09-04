from collections import Counter
import re

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by",
    "for", "from", "had", "has", "have", "he", "her", "his", "in", "is",
    "it", "its", "of", "on", "or", "that", "the", "their", "this", "to",
    "was", "were", "will", "with", "you", "your", "we", "they", "i",
}


def split_sentences(text):
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text.strip()) if sentence.strip()]


def calculate_metrics(text):
    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = split_sentences(text)
    word_count = len(words)
    return {
        "word_count": word_count,
        "character_count": len(text),
        "sentence_count": len(sentences),
        "reading_time": max(1, round(word_count / 200)) if word_count else 0,
    }


def summarize(text, length):
    sentences = split_sentences(text)
    if not sentences:
        return []

    requested_count = {"short": 3, "medium": 4, "detailed": 5}.get(length, 4)
    word_tokens = re.findall(r"\b[a-zA-Z][a-zA-Z'-]+\b", text.lower())
    frequencies = Counter(word for word in word_tokens if word not in STOP_WORDS and len(word) > 2)

    if not frequencies:
        return sentences[:requested_count]

    scored = []
    for index, sentence in enumerate(sentences):
        tokens = re.findall(r"\b[a-zA-Z][a-zA-Z'-]+\b", sentence.lower())
        meaningful = [token for token in tokens if token not in STOP_WORDS and len(token) > 2]
        score = sum(frequencies[token] for token in meaningful) / max(len(meaningful), 1)
        scored.append((score, index, sentence))

    selected = sorted(scored, reverse=True)[:min(requested_count, len(sentences))]
    return [sentence for _, _, sentence in sorted(selected, key=lambda item: item[1])]


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    length = str(payload.get("length", "medium")).lower()

    if not text:
        return jsonify({"error": "Add some text before analyzing it."}), 400

    return jsonify({"metrics": calculate_metrics(text), "summary": summarize(text, length)})


if __name__ == "__main__":
    app.run(debug=True)