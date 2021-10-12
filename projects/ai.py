import speech_recognition as sr
import pyttsx3
# print(sr.Microphone.list_microphone_names())
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
listener = sr.Recognizer()
# listener.energy_threshold = 1200
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        required=0
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "pulse" in name:
                required= index
                print(index)
        with sr.Microphone(device_index=required, chunk_size=1024) as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print('listening...')
            voice = listener.listen(source, timeout=0)
            # command = listener.recognize_google(voice, language = 'en-IN')
            command = listener.recognize_ibm(voice, username='vishal.pvn.edu@gmail.com', password='vishal@IBM21', show_all=True)
            # command = command.lower()
            # if command:
                # command = command.replace('alexa', '')
            print(command)
    except Exception as e:
        print(e)

    # return command


def run_ai():
    pass
    # command = take_command()
    # if 'play' in command:
    #     talk('playing')

while True:
    take_command()
