# PyFAQ — Python FAQ Chatbot

PyFAQ is a web-based FAQ chatbot that helps beginners learn Python programming concepts. It uses Natural Language Processing (NLP) and text similarity to match users' questions with relevant answers from a predefined FAQ knowledge base.

## Features

- Interactive web-based chat interface
- Answers to frequently asked Python questions
- Text preprocessing using NLTK
- TF-IDF vectorization and cosine similarity for question matching
- JSON-based FAQ knowledge base
- Suggested questions for quick access
- Input validation and fallback responses
- Responsive interface for different screen sizes

## Technologies Used

- **Python** — backend logic
- **Flask** — web application framework
- **NLTK** — text preprocessing and stemming
- **Scikit-learn** — TF-IDF vectorization and cosine similarity
- **HTML, CSS and JavaScript** — frontend
- **JSON** — FAQ data storage

## Project Structure

```text
faq_chatbot/
├── app.py
├── faqs.json
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd faq_chatbot
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## How It Works

1. The user enters a question in the chat interface.
2. The application preprocesses the text using tokenization, stopword removal and stemming.
3. TF-IDF converts the question into a numerical representation.
4. Cosine similarity compares the user's question with stored FAQ questions.
5. The chatbot returns the answer associated with the best match or a fallback message when no suitable match is found.

## Example Questions

- What is Python?
- What is a variable in Python?
- Explain lists.
- What is a loop?
- What is a function?

## Future Improvements

- Expand the FAQ knowledge base.
- Improve matching for more varied question wording.
- Add support for additional programming topics.
- Add automated tests for the chatbot API.

## License

This project is intended for educational and learning purposes. Add a license file if you decide to distribute it under a specific open-source license.
