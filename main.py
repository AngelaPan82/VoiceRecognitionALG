import speech_recognition as sr
import time
print("Hi speak to me!")

#trying non-blocking recognition
def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()

recognizer = sr.Recognizer()

with sr.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic, duration=0.1)

# Start listening in the background 
stop_listening = recognizer.listen_in_background(mic, callback)
# This is the main loop
try:

    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    # If keyboard interrupt occurs it stops the program and writes  the following message:
    print("\nProgram stopped by user.")
    stop_listening(wait_for_stop=False)
    time.sleep(1)