import base64
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

PROMPTS = {
    "Summary": """
You are a professional tourist guide.
Provide a high-level overview of "{place}" in {language}.

Focus on:
- The historical significance
- Why the place is famous
- Key architectural or cultural highlights

Keep the explanation concise, engaging, and easy to follow.
Avoid excessive details and dates.
Limit the response to around 200 words.
Respond ONLY in {language}.
""",

    "Detailed": """
You are a professional tourist guide.
Provide a detailed and immersive explanation of "{place}" in {language}.

Cover:
- Historical background and timeline
- Architectural design and unique features
- Cultural importance and notable events
- Interesting facts and visitor insights

Explain concepts clearly and in a storytelling manner.
Include relevant details and examples to create a rich experience.
Limit the response to around 400 words.

Respond ONLY in {language}.
"""
}

def generate_speech(text, voice_id, locale):
    url = "https://global.api.murf.ai/v1/speech/stream"
    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
    "voice_id": voice_id,
    "text": text,
    "locale": locale,
    "model": "FALCON",
    "format": "MP3",
    "sampleRate": 24000,
    "channelType": "MONO"
    }

    response = requests.post(url, headers=headers, json=data, timeout=120)
    response.raise_for_status()
    return response.content


def generate_description(place, answer_type, language):
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured in Backend/.env")
    prompt = PROMPTS[answer_type].format(place=place, language=language)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    return response.text
    
@app.route("/generate-audio-guide", methods=["POST"])
def generate_audio_guide():
    data = request.get_json(silent=True) or {}
    place = data.get("place", "").strip()
    answer_type = data.get("answerType")
    language = data.get("language", "English")
    voice_id = data.get("voiceId")
    locale = data.get("locale")

    if not place:
        return jsonify(error="Choose a destination before generating a guide."), 400
    if answer_type not in PROMPTS:
        return jsonify(error="answerType must be Summary or Detailed."), 400

    try:
        text_description = generate_description(place, answer_type, language)
    except Exception as error:
        app.logger.exception("Guide text generation failed")
        return jsonify(error=f"Could not generate the guide text: {error}"), 502

    result = {"description": text_description, "audioBase64": None}
    if not MURF_API_KEY:
        result["audioError"] = "MURF_API_KEY is not configured; showing the transcript only."
        return jsonify(result)
    if not voice_id or not locale:
        result["audioError"] = "Audio voice settings are missing; showing the transcript only."
        return jsonify(result)

    try:
        audio_bytes = generate_speech(text_description, voice_id, locale)
        result["audioBase64"] = base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as error:
        app.logger.exception("Audio generation failed")
        result["audioError"] = f"Audio generation failed: {error}"
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")