# Text Analyzer & Summarizer

A single-page Flask application that calculates text metrics and creates an extractive summary through a JSON API.

## Run locally

1. Create and activate a virtual environment:

	```powershell
	py -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

2. Install the dependency:

	```powershell
	pip install -r requirements.txt
	```

3. Start the development server:

	```powershell
	py app.py
	```

4. Open `http://127.0.0.1:5000` in a browser.

The backend calculates word, character, sentence, and reading-time metrics and returns 3 to 5 ranked key sentences based on the selected summary length.
