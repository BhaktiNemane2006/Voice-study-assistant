🎤 Voice Study Assistant — Techfest IIT Bombay Hackathon

Built using Murf Falcon – the consistently fastest TTS API

A real-time voice-based AI study companion that listens, understands, and speaks naturally.
Combines Murf Falcon TTS, Deepgram ASR, and Google Gemini AI to create an intelligent, interactive learning experience.

🏆 Hackathon Details

Event: Techfest 2025-26 – Murf AI Voice Agent Hackathon
Institution: IIT Bombay
Category: Voice-Application
Team ID: Murf-250408
Project: Voice Study Assistant

✨ Features
🎧 Two-Way Voice Conversations

Real-time microphone input

Deepgram ASR converts speech to text

Gemini AI understands the question

Murf Falcon generates natural, fast, human-like voice replies

📚 Study-Focused Intelligence

Explains any topic

Generates summaries

Creates quizzes

Revises concepts with you

Reads notes aloud

✔ Additional Features

📝 Persistent conversation history

🎙️ Text + voice input modes

🔒 Secure API Key management with .env

🎵 Auto-play audio TTS output

🔄 Works even without Gemini (fallback rules-based study mode)

🚀 Quick Start
🔧 Prerequisites

Python 3.8+

Microphone (optional, text mode available)

API Keys:

Murf Falcon TTS (Required)

Deepgram ASR (Optional)

Google Gemini (Optional)

📥 Installation
1️⃣ Clone the Repository
git clone https://github.com/BhaktiNemane2006/Voice-study-assistant/edit/main/README.md

🖥️ Backend Setup (Python)
pip install -r requirements.txt

🌐 (Optional) Frontend Setup (React)
cd frontend
npm install
cd ..

🔒 Environment Setup

Duplicate env file:

cp .env.example .env


Add your keys:

ASSEMBLYAI_API_KEY=bfaa55e6ca694a188969b8978bf8a0ed
MURF_API_KEY=ap2_67d7b6be-e74b-4e88-a83c-9b7e8a3cf904
GROQ_API_KEY=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

🔑 Getting API Keys
🎤 Murf Falcon API

Sign up → murf.ai

Go to API settings

Generate a Falcon TTS key

New users get 1,000,000 FREE characters (as per Hackathon rules)

🗣 Deepgram

Sign up → deepgram.com

Free credits for hackathon participants

Get API key from dashboard

🤖 Google Gemini

Visit → Google AI Studio

Generate an API key

Free tier available

▶️ Running the Application

Option A — CLI Version
python voice_assistant.py

CLI Features:

Voice input

Text input

Real-time spoken answers

Study quiz mode

Conversation logging

🧠 How It Works
Voice Flow:

User Speaks → Deepgram ASR → Gemini → Murf Falcon → Spoken Reply

Text Flow:

User Types → Gemini → Murf Falcon → Spoken Reply

Architecture:

Backend: Python (Flask / FastAPI)

ASR: Deepgram

TTS: Murf Falcon

AI Engine: Google Gemini

💡 Use Cases

✔ Study companion
✔ Concept explanations
✔ Summaries & note reading
✔ Audio-based learning for visually impaired users
✔ Flashcards & quizzes
✔ Revision partner
✔ Interactive teaching tool

📁 Project Structure

<img width="604" height="422" alt="image" src="https://github.com/user-attachments/assets/4106b983-2a13-49b3-a988-d75e9991f1d3" />



🔧 Technical Stack
Backend (Python)

Flask / FastAPI

Murf Falcon API

Deepgram ASR

Google Gemini

Python-SocketIO

AI Services Used

Murf Falcon TTS (primary)

Deepgram Nova ASR

Google Gemini 1.5 Flash

📊 Performance

TTS Latency: ~300–500ms (Falcon)

ASR Accuracy: ~95%+

End-to-End Response: 1–2 seconds

Memory footprint: Low

Modes: Text / Voice

📹 Demo Video

🎥 Coming Soon — 

⚙️ Configuration
Environment Variables:
MURF_API_KEY=
DEEPGRAM_API_KEY=
GEMINI_API_KEY=

Backend (app.py) Can Configure:

ASSEMBLYAI_API_KEY=bfaa55e6ca694a188969b8978bf8a0ed
MURF_API_KEY=ap2_67d7b6be-e74b-4e88-a83c-9b7e8a3cf904
GROQ_API_KEY=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

Study modes

Response style

Audio playback settings


🐛 Troubleshooting
❌ Microphone Not Working

Check browser/system permissions

Install:

pip install pyaudio


Linux:

sudo apt install portaudio19-dev

❌ API Key Errors

Check .env format

Ensure no extra spaces

Confirm key validity

❌ No Audio Output

Try different sample rates

Check speaker connection

Restart browser

🤝 Contributing

This is a hackathon project — feel free to fork, remix, and experiment!

👤 Author

Bhakti Anantkumar Nemane Team
Techfest IIT Bombay — Murf AI Voice Agent Hackathon 2025-26
Project: Voice Study Assistant
Team ID: Murf-250408

🙏 Acknowledgments

Murf AI for Falcon TTS

Deepgram for ASR

Google AI for Gemini

Techfest IIT Bombay for organizing this event

Python & React communities

🚀

Built using Murf Falcon – the consistently fastest TTS API
Submission for Techfest IIT Bombay — Murf AI Voice Agent Hackathon 2025-26
