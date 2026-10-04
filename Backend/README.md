# Travel Guide backend setup (Windows)

The frontend sends the selected destination, language, and Summary/Detailed option to `http://127.0.0.1:5000/generate-audio-guide`. Keep this backend running in its own VS Code terminal while the frontend is open.

1. In VS Code, open a terminal and switch to the Backend folder:
   `cd ..\Backend`
2. Create and activate a Python virtual environment, then install dependencies:
   `py -m venv .venv`
   `.\.venv\Scripts\Activate.ps1`
   `py -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env`, then replace the example values with your own Gemini and Murf API keys. Gemini is required to create the transcript; Murf is required to create playable audio.
4. Start the backend:
   `py app.py`
5. In a second VS Code terminal, run the frontend from the Frontend folder:
   `cd ..\Frontend`
   `npm run dev`
6. Open `http://127.0.0.1:5173`, select a destination and Summary or Detailed, then click **Generate Audio Guide**.

If the Gemini key is configured but the Murf key is missing or audio generation fails, the transcript is still returned and the page explains why audio is unavailable. Do not commit your `.env` file or share API keys.
