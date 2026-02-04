from fastapi import FastAPI, HTTPException, UploadFile, File, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import os
from app.inference import predict_from_bytes

# 1. Define your API Key
API_KEY = "sk_hack_9f83kdf93jdf93"

app = FastAPI(title="AI-Generated Voice Detection API")

SUPPORTED_LANGUAGES = {"Tamil", "Telugu", "Hindi", "Malayalam", "English"}

# 2. Request Model
class VoiceJSONRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

# 3. Security Function (Applied to BOTH endpoints)
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        # [cite_start]Returns the exact error format required by the PDF [cite: 32, 86]
        raise HTTPException(status_code=401, detail="Invalid API key or malformed request")
    return x_api_key

# 4. Custom Error Handler (Ensures all errors match the PDF JSON format)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

# ENDPOINT 1: JSON Base64 (STRICTLY REQUIRED FOR HACKATHON)

@app.post("/api/voice-detection", dependencies=[Depends(verify_api_key)])
def voice_detection_json(request: VoiceJSONRequest):
    
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, "Unsupported language")

    if request.audioFormat.lower() != "mp3":
        raise HTTPException(400, "JSON input supports MP3 only")

    try:
        audio_bytes = base64.b64decode(request.audioBase64)
    except Exception:
        raise HTTPException(400, "Invalid Base64 audio")

    # Run Inference
    try:
        classification, confidence, explanation = predict_from_bytes(
            audio_bytes, suffix=".mp3"
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")

    return {
        "status": "success",
        "language": request.language,
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation
    }

# ENDPOINT 2: Multipart Upload (USEFUL FOR YOUR TESTING)

@app.post("/api/voice-detection/upload", dependencies=[Depends(verify_api_key)])
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

    try:
        classification, confidence, explanation = predict_from_bytes(
            audio_bytes, suffix=suffix
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")

    return {
        "status": "success",
        "language": language,
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation
    }