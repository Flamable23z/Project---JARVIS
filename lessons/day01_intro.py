#remember that you must put engine.runAndWait after a speaking block 
import time 
import random 
from datetime import datetime 
from memory import load_memory
from memory import save_memory
from speech import speak
memory = load_memory()
colours = ["blue", "red", "green", "yellow", "orange", "pink", "purple"]
running = True 
hour = datetime.now().hour
def process_command(command):
    ...
def greet_user():
    if "name" in memory:
        if hour < 12:
            speak(f"Good morning {memory["name"]}. What can I help you with today?")
        elif hour < 18:
            speak(f"Good afternoon {memory["name"]}. What can I help you with today?")
            print("Working")
        else:
            speak(f"Good evening {memory["name"]}. What can I help you with today?")
    else:
        name = input("What is your name?")
        memory["name"] = name 
        save_memory(memory)
        if hour < 12:
            speak(f"Good morning {memory["name"]}. It is a pleasure to meet you. What can I help you with today?")
        elif hour < 18:
            speak(f"Good afternoon {memory["name"]}. It is a pleasure to meet you. What can I help you with today?")
        else:
            speak(f"Good evening {memory["name"]}. It is a pleasure to meet you. What can I help you with today?")
greet_user()
while running == True:
    askcommand = input("What can i help you with today?").lower()
    if askcommand == "goodbye" or askcommand == "bye":
        running = False
    else:
        running = True
    if "name" in askcommand and "my" in askcommand:
        print(f"Your name is {memory["name"]}")
    elif "name" in askcommand and "your" in askcommand:
        print(f"My name is Jarvis")
    elif "favourite" in askcommand and "colour" in askcommand and "your" in askcommand:
        if "JARVISfavouritecolour" not in memory:
            JARVISfavouritecolour = random.choice(colours)
            memory["JARVISfavouritecolour"] = JARVISfavouritecolour
            save_memory(memory)
        print(f"My favourite colour is {memory["JARVISfavouritecolour"]}")
    elif "favourite" in askcommand and "colour" in askcommand and "my" in askcommand:
        if "favouritecolour" in memory:
            print(f"Your favourite colour is {memory["favouritecolour"]}")
        else:
            favouritecolour = input("I'm not sure. What is your favourite colour?").lower()
            memory["favouritecolour"] = favouritecolour
            save_memory(memory)
            print(f"Now I know your favourite colour is {memory["favouritecolour"]}")
#remember that you must put engine.runAndWait after a speaking block 