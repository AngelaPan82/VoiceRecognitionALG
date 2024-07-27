import speech_recognition as sr
import time
import threading
import subprocess

print("Hi speak to me!")
#executing function for system commands
def execute_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Command failed with error code {e.returncode}")

def process_audio(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said: " + text)
        if "open google" in text:
            print("Opening web browser")
            #opening the web browser 
            execute_command(["xdg-open", "https://www.google.com/search?q="])
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

#trying non-blocking recognition
#Print is replaced with logging.error because it gives more information for each error and proveds a timestamp
def callback(recognizer, audio):
    threading.Thread(target=process_audio, args=(recognizer,audio)).start()

recognizer = sr.Recognizer()

#starting a seperate thread for adjusting the noise level
with sr.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic,duration=0.1)
    print("Say something!")
    


mic = sr.Microphone()
stop_listening = recognizer.listen_in_background(mic, callback)


try:
    while True:
      #  print("Main loop running")
        time.sleep(0.1)
except KeyboardInterrupt:
    # If keyboard interrupt occurs it stops the program and writes  the following message:
    print("\nProgram stopped by user.")
    stop_listening(wait_for_stop=False)
    time.sleep(1)

