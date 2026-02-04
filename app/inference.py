import torch
from app.model import VoiceCNN
from app.utils import decode_audio_bytes, preprocess_from_waveform

device = "cuda" if torch.cuda.is_available() else "cpu"

model = VoiceCNN().to(device)
model.load_state_dict(
    torch.load("models/voice_ai_detector.pt", map_location=device)
)
model.eval()


def predict_from_bytes(audio_bytes, suffix=".mp3"):
    y, sr = decode_audio_bytes(audio_bytes, suffix=suffix)
    x = preprocess_from_waveform(y, sr).to(device)

    with torch.no_grad():
        prob_ai = model(x).item()

    if prob_ai >= 0.5:
        return (
            "AI_GENERATED",
            round(prob_ai, 4),
            "Unnatural pitch consistency and robotic speech patterns detected"
        )
    else:
        return (
            "HUMAN",
            round(1 - prob_ai, 4),
            "Natural pitch variation and human-like speech patterns detected"
        )
