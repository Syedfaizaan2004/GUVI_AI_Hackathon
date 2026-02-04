from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import base64
import os

API_KEY = "sk_hack_9f83kdf93jdf93"

from app.inference import predict_from_bytes

app = FastAPI(title="AI-Generated Voice Detection API")

SUPPORTED_LANGUAGES = {"Tamil", "Telugu", "Hindi", "Malayalam", "English"}


# ---------- JSON (DEFAULT, MP3 ONLY) ----------
class VoiceJSONRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str


@app.post("/api/voice-detection")
def voice_detection_json(request: VoiceJSONRequest):

    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, "Unsupported language")

    if request.audioFormat.lower() != "mp3":
        raise HTTPException(400, "JSON input supports MP3 only")

    try:
        audio_bytes = base64.b64decode(request.audioBase64)
    except Exception:
        raise HTTPException(400, "Invalid Base64 audio")

    classification, confidence, explanation = predict_from_bytes(
        audio_bytes, suffix=".mp3"
    )

    return {
        "status": "success",
        "language": request.language,
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation
    }


# ---------- MULTIPART (ANY AUDIO FORMAT) ----------
@app.post("/api/voice-detection/upload")
async def voice_detection_multipart(
    language: str,
    file: UploadFile = File(...)
):
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, "Unsupported language")

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(400, "Empty audio file")

    suffix = os.path.splitext(file.filename)[1] or ".wav"

    classification, confidence, explanation = predict_from_bytes(
        audio_bytes, suffix=suffix
    )

    return {
        "status": "success",
        "language": language,
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation
    }
