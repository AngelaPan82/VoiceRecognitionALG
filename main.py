import speech_recognition as sr
import time
import threading

print("Hi speak to me!")

#trying non-blocking recognition
#Print is replaced with logging.error because it gives more information for each error and proveds a timestamp
def callback(recognizer, audio):
    def process_audio():
        print("process_audio triggered")
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    threading.Thread(target=process_audio).start()

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