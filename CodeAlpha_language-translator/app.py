
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "ko": "Korean",
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}

    text = data.get("text", "").strip()
    source = data.get("source", "auto")
    target = data.get("target", "en")

    if not text:
        return jsonify(error="Please enter some text."), 400

    if len(text) > 5000:
        return jsonify(error="Text cannot exceed 5000 characters."), 400

    if client is None:
        return jsonify(error="Gemini API key is not configured."), 500

    target_language = LANGUAGES.get(target)
    if target_language is None:
        return jsonify(error="Unsupported target language."), 400

    if source == "auto":
        source_language = "the detected language"
    else:
        source_language = LANGUAGES.get(source)
        if source_language is None:
            return jsonify(error="Unsupported source language."), 400

    prompt = (
        f"Translate from {source_language} to {target_language}.\n"
        "Return only the translation, without explanations.\n\n"
        f"Text:\n{text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        translated_text = (response.text or "").strip()

        if not translated_text:
            return jsonify(
                error="The translation service returned an empty response."
            ), 502

        return jsonify(translatedText=translated_text)

    except Exception:
        app.logger.exception("Gemini translation request failed")
        return jsonify(
            error="Translation service is temporarily unavailable."
        ), 503


if __name__ == "__main__":
    app.run()
