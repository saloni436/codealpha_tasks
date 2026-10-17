
# Transly — Language Translator

Transly is a web-based language translation application built with Python, Flask, HTML, CSS, and JavaScript. It uses Google's Gemini API to translate text between supported languages.

## Features

- Translate text between supported languages.
- Automatically detect the source language.
- Choose a target language.
- Copy translated text.
- Listen to text using browser text-to-speech, if supported.
- Validate input and display error messages.
- Responsive user interface.

## Technologies Used

- Python
- Flask
- Google Gemini API
- HTML
- CSS
- JavaScript

## Supported Languages

- English
- Hindi
- French
- Spanish
- German
- Korean

## Installation

1. Clone this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

4. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root and add your own Gemini API key:

   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

7. Start the application:

   ```powershell
   python app.py
   ```

8. Open the local address shown in the terminal.

## Security

Keep your `.env` file private. Never upload your API key to GitHub.

## Purpose

This project demonstrates API integration and full-stack web development using Python and frontend technologies.
