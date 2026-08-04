import os
import json 
import pyttsx3
import time 
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 185)
def speak(text):
    engine.say(text)
    engine.runAndWait()
def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as file:
            return json.load(file)  
    else:
        return {}
def save_memory(memory):
    with open("memory.json", "w") as file:
       json.dump(memory, file, indent = 4)
memory = load_memory()
def start_jarvis():
    if "name" in memory:
        speak(f"Welcome back {memory["name"]}. What would you like me to assist you with today?")
    else:
        name = input("What is your name?")
        memory["name"] = name 
        save_memory(memory)
        speak(f"Hello {name}, I am Jarvis")
        speak("Nice to meet you")
start_jarvis()
