import speech_recognition as sr
import time
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("Hi speak to me!")

#trying non-blocking recognition
#Print is replaced with logging.error because it gives more information for each error and proveds a timestamp
def callback(recognizer, audio):
    logging.debug("it works?")
    def process_audio(recognizer, audio):
        logging.debug("Audio recieved?")
        try:
            text = recognizer.recognize_google(audio)
            logging.info("You said: " + text)
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))

    threading.Thread(target=process_audio, args=(recognizer, audio)).start()



def adjusting_noise_level(mic, recognizer):
    while True:
        logging.debug("Adjusting noise level")
        recognizer.adjust_for_ambient_noise(mic, duration=0.1)
        time.sleep(1)

recognizer = sr.Recognizer()

#r = sr.Recognizer()
#starting a seperate thread for adjusting the noise level
with sr.Microphone() as mic:
    logging.info("Microphone is working")
    noise_thread = threading.Thread(target=adjusting_noise_level, args=(mic, recognizer))
    noise_thread.daemon=True
    noise_thread.start()
    logging.info("Say something!")


# Start listening in the background 
stop_listening = recognizer.listen_in_background(mic, callback)
logging.info("Listening in the background.")

# This is the main loop
try:
    while True:
        logging.debug("Main loop is running. !!!!")
        time.sleep(0.1)
except KeyboardInterrupt:
    # If keyboard interrupt occurs it stops the program and writes  the following message:
    logging.info("\nProgram stopped by user.")
    stop_listening(wait_for_stop=False)
    time.sleep(1)