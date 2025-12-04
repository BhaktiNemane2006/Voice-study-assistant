import os
import time
import wave

import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
import requests
from dotenv import load_dotenv

from groq import Groq
from murf import Murf


# ------------- 1. LOAD ENV VARIABLES -------------

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not ASSEMBLYAI_API_KEY or not MURF_API_KEY or not GROQ_API_KEY:
    raise ValueError(
        "Please set ASSEMBLYAI_API_KEY, MURF_API_KEY, and GROQ_API_KEY in your .env file"
    )

# Groq client (for study explanations)
groq_client = Groq(api_key=GROQ_API_KEY)

# Murf client (for Falcon TTS)
murf_client = Murf(
    api_key=MURF_API_KEY,  # default base URL = api.murf.ai
)



# ------------- 2. AUDIO RECORDING HELPERS -------------

SAMPLE_RATE = 16_000   # 16 kHz is fine for ASR
CHANNELS = 1


def record_question(duration=8):
    """
    Record audio and save to a uniquely named WAV file.
    """
    input("\nPress ENTER and then start speaking your question...")

    filename = f"question_{int(time.time())}.wav"  # unique filename

    print(f"🎙️  Recording for {duration} seconds...")
    recording = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )
    sd.wait()

    write(filename, SAMPLE_RATE, recording)
    print(f"✅ Recording saved to {filename}")

    return filename



# ------------- 3. ASSEMBLYAI SPEECH-TO-TEXT -------------

ASSEMBLYAI_TRANSCRIPT_URL = "https://api.assemblyai.com/v2/transcript"
ASSEMBLYAI_UPLOAD_URL = "https://api.assemblyai.com/v2/upload"

assemblyai_headers = {
    "authorization": ASSEMBLYAI_API_KEY,
}


def upload_to_assemblyai(audio_path: str) -> str:
    """
    Upload local audio file to AssemblyAI and return upload_url.
    """
    print("⬆️  Uploading audio to AssemblyAI...")
    with open(audio_path, "rb") as f:
        response = requests.post(
            ASSEMBLYAI_UPLOAD_URL,
            headers=assemblyai_headers,
            data=f
        )
    response.raise_for_status()
    upload_url = response.json()["upload_url"]
    print("✅ Uploaded.")
    return upload_url


def transcribe_with_assemblyai(audio_path: str) -> str:
    """
    Send audio file to AssemblyAI, poll until transcription is ready,
    then return transcribed text.
    """
    upload_url = upload_to_assemblyai(audio_path)

    # Create transcript job
    print("📝 Creating transcription job...")
    transcript_request = {
        "audio_url": upload_url,
        "language_code": "en",
    }

    response = requests.post(
        ASSEMBLYAI_TRANSCRIPT_URL,
        json=transcript_request,
        headers=assemblyai_headers,
    )
    response.raise_for_status()
    transcript_id = response.json()["id"]
    print(f"📄 Transcript id: {transcript_id}")

    # Poll for completion
    while True:
        poll_response = requests.get(
            f"{ASSEMBLYAI_TRANSCRIPT_URL}/{transcript_id}",
            headers=assemblyai_headers,
        )
        poll_response.raise_for_status()
        status = poll_response.json()["status"]

        if status == "completed":
            text = poll_response.json()["text"]
            print(f"✅ Transcription: {text}")
            return text
        elif status == "error":
            print("❌ Transcription failed:", poll_response.json())
            raise RuntimeError("AssemblyAI transcription error")

        print("⏳ Waiting for transcription...")
        time.sleep(2)


# ------------- 4. STUDY ANSWER USING GROQ (LLAMA 3) -------------

def get_study_answer(question: str) -> str:
    """
    Use Groq (Llama 3.1 8B Instant) to generate a simple study explanation.
    """
    print("\n🤖 Generating study explanation...")

    prompt = (
        "You are a friendly Voice Study Assistant for a college student. "
        "Explain concepts in very simple English, with short sentences. "
        "If the question is about definitions, give examples too. "
        "If the question is not related to studies, answer briefly and bring them back to study topics.\n\n"
        f"Student question: {question}"
    )

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ new recommended model
        messages=[
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
    )

    answer = response.choices[0].message.content.strip()
    print("📚 Answer:", answer)
    return answer



# ------------- 5. MURF FALCON TEXT-TO-SPEECH -------------

def speak_with_murf(text: str):
    """
    Use Murf Text-to-Speech to turn text into speech and play it.
    Uses the non-streaming /v1/speech/generate endpoint under the hood.
    """
    print("\n🗣️  Converting answer to speech with Murf...")

    # Call Murf TTS via SDK (non-streaming Gen2)
    tts_response = murf_client.text_to_speech.generate(
        text=text,
        voice_id="en-US-terrell",   # you can change this to any valid Murf voice
        format="MP3",
        sample_rate=44100.0,
    )

    # The SDK wraps the HTTP response. It exposes the audio file URL
    # as `audio_file` (snake_case of "audioFile" from the HTTP API).
    audio_url = getattr(tts_response, "audio_file", None)

    if not audio_url:
        print("⚠️ Murf TTS response did not contain an audio URL.")
        print("   Raw response:", tts_response)
        return

    print(f"✅ Murf returned audio URL: {audio_url}")

    # Download the audio file
    try:
        audio_resp = requests.get(audio_url)
        audio_resp.raise_for_status()
    except Exception as e:
        print("❌ Failed to download audio from Murf:", e)
        return

    # Save as local MP3 file
    local_path = "murf_output.mp3"
    with open(local_path, "wb") as f:
        f.write(audio_resp.content)

    print(f"✅ Audio downloaded to {local_path}")
    print("▶️ Playing answer...")
    try:
        playsound(local_path)
        print("🔚 Finished playing.\n")
    except Exception as e:
        print("⚠️ Could not play audio:", e)



# ------------- 6. MAIN LOOP -------------

def main():
    print("========================================")
    print(" 🎓 Voice Study Assistant (Terminal) ")
    print(" Say 'exit' or 'quit' in your question to stop.")
    print("========================================")

    while True:
        # 1. Record question
        audio_file = record_question(duration=8)  # 8 seconds per question

        # 2. Transcribe with AssemblyAI
        try:
            question_text = transcribe_with_assemblyai(audio_file)
        except Exception as e:
            print("Error during transcription:", e)
            continue

        if not question_text:
            print("I didn't catch that. Please try again.")
            continue

        # Exit condition
        lower_q = question_text.lower()
        if "exit" in lower_q or "quit" in lower_q or "stop" in lower_q:
            print("👋 Bye! Happy studying.")
            break

        # 3. Get AI answer (Groq)
        try:
            answer_text = get_study_answer(question_text)
        except Exception as e:
            print("Error from AI model:", e)
            continue

        # 4. Speak answer with Murf
        try:
            speak_with_murf(answer_text)
        except Exception as e:
            print("Error speaking with Murf:", e)

        # small pause between questions
        time.sleep(1)


if __name__ == "__main__":
    main()

