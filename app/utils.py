import os
import uuid
import librosa
import numpy as np
import torch
import miniaudio

SAMPLE_RATE = 16000
N_MELS = 128
HOP_LENGTH = int(0.01 * SAMPLE_RATE)
N_FFT = int(0.025 * SAMPLE_RATE)
FIXED_FRAMES = 300
MIN_DURATION = 2.0
MAX_DURATION = 6.0

TMP_DIR = "_tmp_audio"
os.makedirs(TMP_DIR, exist_ok=True)


def decode_audio_bytes(audio_bytes, suffix=".mp3"):
    """
    Decode audio bytes by writing to a temporary file.
    REQUIRED for MP3/Base64 with librosa on Windows.
    """
    temp_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}{suffix}")

    with open(temp_path, "wb") as f:
        f.write(audio_bytes)

    try:
        # Use miniaudio for robust decoding (no ffmpeg dependency required)
        decoded = miniaudio.decode_file(temp_path)
        
        # Convert to numpy float32 (miniaudio returns int16 usually)
        y = np.array(decoded.samples, dtype=np.float32) / 32768.0
        
        # Handle channels (convert to mono if needed)
        if decoded.nchannels > 1:
            y = y.reshape(-1, decoded.nchannels)
            y = y.mean(axis=1) # Average channels to get mono
            
        sr = decoded.sample_rate
        return y, sr
    except Exception as e:
        # Fallback or re-raise
        raise ValueError(f"Failed to decode audio: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def preprocess_from_waveform(y, sr):
    if sr != SAMPLE_RATE:
        y = librosa.resample(y, orig_sr=sr, target_sr=SAMPLE_RATE)

    duration = len(y) / SAMPLE_RATE
    if duration < MIN_DURATION:
        raise ValueError("Audio too short (<2s)")

    if duration > MAX_DURATION:
        y = y[:int(MAX_DURATION * SAMPLE_RATE)]

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        center=False
    )

    mel = librosa.power_to_db(mel, ref=np.max)

    if mel.shape[1] >= FIXED_FRAMES:
        mel = mel[:, :FIXED_FRAMES]
    else:
        mel = np.pad(
            mel,
            ((0, 0), (0, FIXED_FRAMES - mel.shape[1])),
            mode="constant"
        )

    return torch.tensor(mel).unsqueeze(0).unsqueeze(0).float()
