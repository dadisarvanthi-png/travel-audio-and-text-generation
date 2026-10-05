# Travel Guide

A small full-stack travel guide app. Choose a destination, select a summarized or detailed guide, and generate a spoken audio version in English, Hindi, Tamil, or Telugu.

## Features

- Browse featured Indian destinations or search for another destination.
- Generate a concise summary or a more detailed guide with Gemini.
- Choose a language and voice for audio generation with Murf.
- Read the generated transcript and play the audio in the browser.

## Requirements

- Python 3.10 or later
- Node.js 18 or later
- Gemini API key for guide text
- Murf API key for generated audio

## Setup on Windows

### 1. Configure and start the backend

From the repository root, open a terminal and run:

```powershell
cd Backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `Backend/.env` and set your own API keys:

```text
GEMINI_API_KEY=your_gemini_api_key
MURF_API_KEY=your_murf_api_key
FLASK_DEBUG=0
```

Start the backend from the `Backend` folder:

```powershell
py app.py
```

The backend listens at `http://127.0.0.1:5000`. Keep this terminal running. The local `.env` file is ignored by Git—never commit or share it.

### 2. Start the frontend

Open a second terminal at the repository root:

```powershell
cd Frontend
npm run dev
```

Open `http://127.0.0.1:5173` in a browser. No npm package installation is needed for the frontend dev server.

## Use the app

1. Click a featured destination, or search for a place.
2. Choose **Summarized** or **Detailed**.
3. Select a language and voice.
4. Click **Generate Audio Guide**. The transcript appears in the panel and generated audio can be played there.

Gemini is required to generate the transcript. Murf is required for playable audio. If audio generation is unavailable, the app can still return the transcript when Gemini is configured.

## API

The frontend sends a `POST` request to `http://127.0.0.1:5000/generate-audio-guide` with a JSON body similar to:

```json
{
  "place": "Taj Mahal",
  "answerType": "Summary",
  "language": "English",
  "voiceId": "Matthew",
  "locale": "en-US"
}
```

`answerType` must be `Summary` or `Detailed`. A successful response includes the generated `description` and, when available, base64-encoded MP3 audio in `audioBase64`.

## Deploy to Render

The repository includes a Render Blueprint in `render.yaml`. It deploys the frontend and Flask API together as one Python web service, so the browser can call the API on the same origin.

1. Push this repository to GitHub.
2. In Render, choose **New → Blueprint**, connect GitHub, and select this repository.
3. Review the service named `travel-guide`. Render reads the build/start commands from `render.yaml`.
4. Enter `GEMINI_API_KEY` and `MURF_API_KEY` in Render when prompted, then create the service.
5. Open the service's public URL when the deployment finishes.

Do not put secrets in `render.yaml`, commit `Backend/.env`, or paste keys into source files. Add production keys only in Render's environment-variable settings. The Blueprint selects Render's free plan; free services can spin down when idle, so the first request after inactivity may take longer.

## Troubleshooting

- **Cannot connect to the backend:** confirm `py app.py` is still running in the Backend terminal.
- **Gemini key not configured:** confirm the key is in `Backend/.env`, then restart the backend.
- **Transcript works but audio does not:** check the Murf key and the backend terminal for the provider error.
- **Port already in use:** stop the other process using port `5000` or `5173`, then restart the corresponding server.
