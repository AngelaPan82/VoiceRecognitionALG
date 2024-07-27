import speech_recognition as sr
import time
import threading
import subprocess
import platform

print("Hi speak to me!")

user_voice_prints ={
    "user1":"This is sample for user1",
    "user2":"This is sample for user2"
}
#Funcion to simulate the creation of a voice print
def create_voice_print(audio):
    return "this is a sample voice print"

#Function voice proint verification
def verify_voice_print(audio, stored_voice_print):
    return create_voice_print(audio) == stored_voice_print

#Second factor authentication its not a must but it is a good practice
def verify_second_factor_print(audio, second_factor):
    return second_factor == "1234"


#executing function for system commands
def execute_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")

def process_audio(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said: " + text)

        user_id = "user1"
        if verify_voice_print(audio, user_voice_prints[user_id]):
            print("Voice print verified")
        #Time for the second factor
            second_factor = input("Enter PIN: ")
            if verify_second_factor_print(audio, second_factor):
                print("Second factor verified")
                if "open google" in text or "open web browser" in text:
                    print("Opening web browser")
                    if platform.system() == "Windows":
                        execute_command(["start", "chrome"])
                    elif platform.system() == "Linux":
                        execute_command(["google-chrome"])
                    elif platform.system() == "Darwin":
                        execute_command(["open -a", "Google Chrome"])  
                else:
                    print("Second factor authentication failed")
            else:
                 print("Voice authentication failed")
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

