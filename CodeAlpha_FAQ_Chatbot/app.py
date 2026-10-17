
import json
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

FAQ_FILE = Path(__file__).parent / "faqs.json"

with FAQ_FILE.open(encoding="utf-8") as file:
    faqs = json.load(file)

stemmer = PorterStemmer()

STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "what", "who", "how", "do", "does", "did", "can",
    "in", "on", "at", "to", "of", "for", "and", "or",
    "i", "you", "your", "it", "with", "please", "explain",
}


def preprocess(text):
    """Tokenize text, remove stopwords, and stem words."""
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return " ".join(
        stemmer.stem(word)
        for word in words
        if word not in STOPWORDS
    )


faq_questions = [faq["question"] for faq in faqs]
processed_questions = [preprocess(question) for question in faq_questions]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
question_vectors = vectorizer.fit_transform(processed_questions)

SIMILARITY_THRESHOLD = 0.22

FALLBACK_ANSWER = (
    "Sorry, I couldn't find a suitable answer. Try asking about "
    "Python basics, variables, lists or functions."
)


def find_answer(user_text):
    """Return the answer to the most similar FAQ question."""
    processed_text = preprocess(user_text)

    if not processed_text:
        return {
            "answer": "Please ask a question about Python programming.",
            "matched": False,
        }

    user_vector = vectorizer.transform([processed_text])
    similarities = cosine_similarity(user_vector, question_vectors)[0]

    best_index = similarities.argmax()
    best_score = float(similarities[best_index])

    if best_score < SIMILARITY_THRESHOLD:
        return {"answer": FALLBACK_ANSWER, "matched": False}

    return {
        "answer": faqs[best_index]["answer"],
        "matched": True,
        "similarity": round(best_score, 3),
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_text = data.get("message", "")

    if not isinstance(user_text, str):
        return jsonify(error="Message must be text."), 400

    user_text = user_text.strip()

    if not user_text:
        return jsonify(error="Please enter a question."), 400

    if len(user_text) > 500:
        return jsonify(
            error="Please keep your question under 500 characters."
        ), 400

    return jsonify(find_answer(user_text))


@app.route("/health")
def health():
    return jsonify(status="ok", faq_count=len(faqs))


if __name__ == "__main__":
    app.run()
