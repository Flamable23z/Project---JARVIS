import time 
import random 
import requests
from datetime import datetime 
from memory import load_memory, save_memory
from speech import speak

# -------------------------------------------------------------
# 1. INITIAL SETUP & MEMORY
# -------------------------------------------------------------
memory = load_memory()
colours = ["blue", "red", "green", "yellow", "orange", "pink", "purple"]
running = True 
hour = datetime.now().hour

# -------------------------------------------------------------
# 2. SURF SKILL FUNCTION (Muizenberg & Rondebosch Schedule)
# -------------------------------------------------------------
def check_surf():
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": -34.1081,
        "longitude": 18.4719,
        "hourly": ["wave_height", "wave_period", "wave_direction"],
        "timezone": "Africa/Johannesburg"
    }
    
    print("Jarvis: Checking Muizenberg conditions for tomorrow morning...")
    speak("Checking the swell report at Muizenberg.")
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Look at 06:00 AM forecast (Index 6)
        morning_height = data["hourly"]["wave_height"][6]
        morning_period = data["hourly"]["wave_period"][6]
        
        print(f"Forecast at 06:00 AM: {morning_height}m swell | {morning_period}s period")
        
        # Condition Check: Swell >= 1.2m and Period >= 10s
        if morning_height >= 1.2 and morning_period >= 10:
            surf_message = (
                f"Surf is pumping at Muizenberg! Swell is {morning_height} meters "
                f"with a {morning_period} second period. "
                "Wake up at 5:30 AM to surf before Rondebosch starts at 8:00."
            )
            print(f"Jarvis: {surf_message}")
            speak("Surf's up! Conditions look great. I sent an alert to your phone to set your alarm for 5:30 AM.")
            
            # Send alert to iPhone via ntfy
            requests.post(
                "https://ntfy.sh/muizenberg_surf_benjy",
                data=surf_message.encode("utf-8")
            )
        else:
            flat_message = (
                f"Conditions are small (Height: {morning_height}m, Period: {morning_period}s). "
                "Sleep in. Regular alarm at 7:00 AM."
            )
            print(f"Jarvis: {flat_message}")
            speak("Conditions aren't ideal today. Sleep in, regular alarm at 7:00 AM.")
            
    except Exception as e:
        print(f"Error fetching surf data: {e}")
        speak("I had trouble reaching the weather service.")

# -------------------------------------------------------------
# 3. GREET USER
# -------------------------------------------------------------
def greet_user():
    if "name" in memory:
        user_name = memory['name']
        if hour < 12:
            greeting = f"Good morning {user_name}."
        elif hour < 18:
            greeting = f"Good afternoon {user_name}."
        else:
            greeting = f"Good evening {user_name}."
            
        print(greeting)
        speak(f"{greeting} What can I help you with today?")
    else:
        name = input("What is your name? ")
        memory["name"] = name 
        save_memory(memory)
        
        if hour < 12:
            greeting = f"Good morning {name}. It is a pleasure to meet you."
        elif hour < 18:
            greeting = f"Good afternoon {name}. It is a pleasure to meet you."
        else:
            greeting = f"Good evening {name}. It is a pleasure to meet you."
            
        print(greeting)
        speak(greeting)

greet_user()

# -------------------------------------------------------------
# 4. MAIN COMMAND LOOP
# -------------------------------------------------------------
while running:
    askcommand = input("\nWhat can I help you with today? ").lower().strip()
    
    if askcommand in ["goodbye", "bye", "exit", "quit"]:
        speak("Goodbye!")
        print("Goodbye!")
        running = False
        
    elif "surf" in askcommand or "swell" in askcommand or "waves" in askcommand:
        check_surf()
        
    elif "name" in askcommand and "my" in askcommand:
        response = f"Your name is {memory.get('name', 'unknown')}."
        print(response)
        speak(response)
        
    elif "name" in askcommand and "your" in askcommand:
        print("My name is Jarvis.")
        speak("My name is Jarvis.")
        
    elif "favourite" in askcommand and "colour" in askcommand and "your" in askcommand:
        if "JARVISfavouritecolour" not in memory:
            memory["JARVISfavouritecolour"] = random.choice(colours)
            save_memory(memory)
        response = f"My favourite colour is {memory['JARVISfavouritecolour']}."
        print(response)
        speak(response)
        
    elif "favourite" in askcommand and "colour" in askcommand and "my" in askcommand:
        if "favouritecolour" in memory:
            response = f"Your favourite colour is {memory['favouritecolour']}."
            print(response)
            speak(response)
        else:
            favouritecolour = input("I'm not sure. What is your favourite colour? ").lower()
            memory["favouritecolour"] = favouritecolour
            save_memory(memory)
            response = f"Now I know your favourite colour is {favouritecolour}."
            print(response)
            speak(response)
            
    elif "time" in askcommand:
        current_time = datetime.now().strftime("%I:%M %p")
        print(current_time)
        speak(f"The time is {current_time}")
        
    elif askcommand == "new user":
        memory.pop("name", None)
        name = input("What is your name? ")
        memory["name"] = name 
        save_memory(memory)
        print(f"Hello {name}, memory updated.")
        speak(f"Hello {name}, memory updated.")