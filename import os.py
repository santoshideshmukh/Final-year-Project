import os
import speech_recognition as sr
from google.cloud import speech
from datetime import datetime

# Initialize Google Cloud Speech Client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path_to_your_credentials.json"
client = speech.SpeechClient()

# Initialize SpeechRecognition
recognizer = sr.Recognizer()

# Function to transcribe speech to text
def transcribe_audio(audio_file):
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        print("Transcribing...")

        # Recognize using Google Speech API
        response = recognizer.recognize_google(audio)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to store transcript in the database
def store_transcript(patient_id, doctor_id, transcript):
    import sqlite3
    conn = sqlite3.connect("ehr_transcripts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            doctor_id TEXT,
            transcript TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()

    cursor.execute("INSERT INTO transcripts (patient_id, doctor_id, transcript, timestamp) VALUES (?, ?, ?, ?)",
                   (patient_id, doctor_id, transcript, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Main Function
if __name__ == "__main__":
    print("Listening for audio...")
    file_path = input("Enter the path to the audio file: ")
    patient_id = input("Enter Patient ID: ")
    doctor_id = input("Enter Doctor ID: ")

    # Transcribe
    transcript = transcribe_audio(file_path)

    if transcript:
        print(f"Transcript: {transcript}")
        store_transcript(patient_id, doctor_id, transcript)
        print("Transcript saved successfully!")
    else:
        print("No transcription available.")
