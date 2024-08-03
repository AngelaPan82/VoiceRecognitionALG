import speech_recognition as sr
import subprocess
import platform

print("Hi speak to me!")

#user_voice_prints ={
 #   "user1":"user one",
#}

expected_pin = "1234"

#executing function for system commands
def execute_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")

def process_audio(text):
    if "open google" in text or "open web browser" in text:
        print("Opening web browser...")
        if platform.system()== "Windows":
            execute_command("start chrome")
        elif platform.system() == "Linux":
            execute_command("google-chrome")
        elif platform.system() == "Darwin":
            execute_command("open -a 'Google Chrome")

recognizer = sr.Recognizer()

#starting a seperate thread for adjusting the noise level
def recognize_audio():
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic,duration=0.1)
        print("Say something!")
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio).lower()
            print("You said: "+ text)
            return audio, text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None, None
        except sr.RequestError as e:
            print(f"Could not request results from Google speech recognition service:")
            return None, None
try:   
    while True:
        audio, command_text = recognize_audio()
        if audio and command_text:
            second_factor = input("Enter PIN:")
            if second_factor == expected_pin:
                print("Second factor verified.")
                process_audio(command_text)
            else:
                print("Second factor authentication failed.")
        else:
            print("Please try again.")
           
        user_input = input("Do you want to continue ? (yes/no):").strip().lower()
        if user_input != 'yes':
            print("Program stopped by user")
            break
except KeyboardInterrupt:
        print("Program stopped by user")