import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()