import speech_recognition as sr
import pyttsx3

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech_from_mic():
    """Capture speech input from the microphone."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Request error. Please check your internet connection."

# Simulated Conversation
print("Doctor-Patient Conversation Simulation")
speak("Hello, I am your virtual doctor. How can I help you today?")

while True:
    print("You (Patient):")
    patient_input = recognize_speech_from_mic()
    print(f"Patient: {patient_input}")

    if "bye" in patient_input.lower():
        speak("Goodbye! Take care.")
        print("Doctor: Goodbye! Take care.")
        break

    # Example of doctor responding to patient inputs
    if "fever" in patient_input.lower():
        response = "It seems like you have a fever. Have you taken any medication?"
    elif "headache" in patient_input.lower():
        response = "For headaches, staying hydrated and resting can help. Have you experienced this before?"
    else:
        response = "Can you tell me more about your symptoms?"

    print(f"Doctor: {response}")
    speak(response)