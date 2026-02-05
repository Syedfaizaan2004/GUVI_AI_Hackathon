# AI-Generated Voice Detection API 🎙️🚫🤖

A secure, RESTful API built with **FastAPI** and **PyTorch** to detect whether a voice recording is Human or AI-Generated. This solution was developed for the **GUVI AI Hackathon**.

---

## 🔗 Live Demo (For Judges)

* **Base URL:** `https://your-app-name.onrender.com` *(Replace with your actual Live URL)*
* **Test Endpoint:** `/api/voice-detection`
* **API Key:** `sk_hack_9f83kdf93jdf93`

---

## 🚀 Features

* **Dual Mode Inference:** Supports both JSON (Base64 encoded) and standard File Uploads.
* **Multi-Language Support:** Optimized for **Tamil, English, Hindi, Malayalam, and Telugu**.
* **Secure:** Protected via `x-api-key` header authentication.
* **Robust AI Model:** Uses a custom **CNN (Convolutional Neural Network)** trained on Mel-spectrograms.
* **Standardized Output:** Returns strict JSON responses compliant with hackathon guidelines.
* **Machine Learning:** I have trained the large amount of data of differnt audio of human and ai voice using audioCNN Mel - Spectrogram deep learning model. It got 96% accuracy. So it is a good ml.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ML Backend:** PyTorch, Librosa, NumPy
* **Audio Processing:** Miniaudio (FFmpeg-free decoding)
* **Deployment:** Docker / Render / Hugging Face Spaces

---

## 📂 Project Structure

```text
📦 voice-ai-detector
├── 📂 app
│   ├── 📜 main.py       # API Endpoints & Security Logic
│   ├── 📜 model.py      # VoiceCNN PyTorch Model Architecture
│   ├── 📜 inference.py  # Prediction Logic & Preprocessing
│   └── 📜 utils.py      # Audio decoding helper functions
├── 📂 models
│   └── 📜 voice_ai_detector.pt  # Trained Model Weights
├── 📜 requirements.txt  # Python Dependencies
├── 📜 Dockerfile        # Container configuration
├── 📜 LICENSE           # MIT License
└── 📜 README.md         # Documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/voice-ai-detector.git
cd voice-ai-detector
```

### 2. Create a Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

This API is protected by an API Key. You must set it as an environment variable for security.

**Linux/Mac:**
```bash
export API_KEY="your_secret_key_here"
```

**Windows (PowerShell):**
```powershell
$env:API_KEY="your_secret_key_here"
```

> **Note:** If no key is set, the application defaults to `sk_hack_9f83kdf93jdf93` for local testing.

---

## 🏃‍♂️ Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be live at `http://localhost:8000`.

---

## 📖 API Documentation

### 1. Detect Voice (JSON Base64) - Hackathon Standard
Accepts a Base64-encoded MP3 string.

* **URL:** `/api/voice-detection`
* **Method:** `POST`
* **Headers:**
    * `Content-Type: application/json`
    * `x-api-key: <YOUR_API_KEY>`

**Request Body:**
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "SUQzBAAAAAAAI1..." 
}
```

**Response (Success):**
```json
{
    "status": "success",
    "language": "English",
    "classification": "AI_GENERATED",
    "confidenceScore": 0.98,
    "explanation": "Unnatural pitch consistency and robotic speech patterns detected"
}
```

**cURL Test Example:**
```bash
curl -X POST http://localhost:8000/api/voice-detection \
-H "Content-Type: application/json" \
-H "x-api-key: sk_hack_9f83kdf93jdf93" \
-d '{"language": "Tamil", "audioFormat": "mp3", "audioBase64": "<BASE64_STRING>"}'
```

### 2. Upload Audio File (Multipart) - For Testing
Allows direct file uploads for easier testing.

* **URL:** `/api/voice-detection/upload`
* **Method:** `POST`
* **Headers:**
    * `x-api-key: <YOUR_API_KEY>`

**cURL Test Example:**
```bash
curl -X POST http://localhost:8000/api/voice-detection/upload \
-H "x-api-key: sk_hack_9f83kdf93jdf93" \
-F "language=Hindi" \
-F "file=@./test_audio.mp3"
```