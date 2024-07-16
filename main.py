# Verify distutils installation
try:
    import distutils
    print("distutils installed successfully")
except ImportError:
    print("distutils is not installed")
    # If distutils is not installed, you can install it using pip
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])

# Import necessary modules
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()

            print(f"Recognized: {text}")

    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        continue
