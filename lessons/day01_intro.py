import time 
import random 
import requests
from datetime import datetime 
from memory import load_memory, save_memory
from speech import speak

memory = load_memory()
colours = ["blue", "red", "green", "yellow", "orange", "pink", "purple"]
running = True 
hour = datetime.now().hour

# Helper function to check a single beach
def check_single_beach(lat, lon, min_wind, max_wind, is_or_range, beach_name):
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["wave_height", "wave_period", "wind_speed_10m", "wind_direction_10m", "sea_surface_temperature"],
        "timezone": "Africa/Johannesburg"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # 06:00 AM forecast (Index 6)
        height = data["hourly"]["wave_height"][6]
        period = data["hourly"]["wave_period"][6]
        wind = data["hourly"]["wind_speed_10m"][6]
        wind_dir = data["hourly"]["wind_direction_10m"][6]
        temp = data["hourly"]["sea_surface_temperature"][6]
        
        # Defensive checks for None
        if wind is None: wind = 0
        if wind_dir is None: wind_dir = 0
        if temp is None: temp = 15
        
        # Check offshore wind range
        if is_or_range:
            is_offshore = (wind_dir >= min_wind or wind_dir <= max_wind) # e.g. Muizenberg NW-NE
        else:
            is_offshore = (min_wind <= wind_dir <= max_wind)             # e.g. Llandudno SE
            
        # Realistic surf conditions check
        is_good = (height >= 0.8 and period >= 7.0 and wind < 22 and is_offshore)
        
        stats = f"{beach_name.capitalize()}: {height}m ({period}s) | Wind: {wind}km/h ({wind_dir}°) | Water: {temp}°C"
        return is_good, stats
        
    except Exception as e:
        print(f"Error checking {beach_name}: {e}")
        return False, f"{beach_name.capitalize()}: Data unavailable"

# Main multi-beach surf skill
def check_surf():
    print("Jarvis: Checking Muizenberg and Llandudno forecasts...")
    speak("Checking surf conditions for both Muizenberg and Llandudno.")
    
    # 1. Check Muizenberg (NW to NE offshore)
    muiz_good, muiz_stats = check_single_beach(-34.1081, 18.4719, 315, 45, True, "muizenberg")
    
    # 2. Check Llandudno (SE offshore)
    llan_good, llan_stats = check_single_beach(-34.0083, 18.3383, 112, 157, False, "llandudno")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Decision tree
    if muiz_good and llan_good:
        status = "BOTH GOOD"
        msg = f"Surf's UP everywhere! Both spots are firing.\n{muiz_stats}\n{llan_stats}\nSet alarm for 5:30 AM!"
        speak("Great news! Both Muizenberg and Llandudno have good waves tomorrow morning.")
    elif muiz_good:
        status = "MUIZENBERG GOOD"
        msg = f"Surf's UP at Muizenberg! {muiz_stats}. Set alarm for 5:30 AM!"
        speak("Muizenberg is looking good! Wind is offshore on the False Bay side.")
    elif llan_good:
        status = "LLANDUDNO GOOD"
        msg = f"Surf's UP at Llandudno! {llan_stats}. Set alarm for 5:30 AM!"
        speak("Llandudno is looking good! South East wind is clean on the Atlantic side.")
    else:
        status = "SLEEP IN"
        msg = f"Neither beach is ideal.\n{muiz_stats}\n{llan_stats}"
        speak("Conditions aren't ideal at either beach tomorrow. Sleep in!")
        
    print(f"\nJarvis Report:\n{msg}")
    
    # Send iPhone alert if either spot is good
    if muiz_good or llan_good:
        requests.post(
            "https://ntfy.sh/muizenberg_surf_benjy",
            data=msg.encode("utf-8")
        )

    # Log entry to history file
    log_entry = f"[{timestamp}] Result: {status}\n  -> {muiz_stats}\n  -> {llan_stats}\n"
    with open("surf_history.txt", "a", encoding="utf-8", errors="replace") as file:
        file.write(log_entry)

# Greeting setup
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

# Main command loop
while running:
    askcommand = input("\nWhat can I help you with today? ").lower().strip()
    
    if askcommand in ["goodbye", "bye", "exit", "quit"]:
        speak("Goodbye!")
        print("Goodbye!")
        running = False
        
    elif "surf" in askcommand or "swell" in askcommand or "waves" in askcommand:
        check_surf()
        
    elif "history" in askcommand or "log" in askcommand:
        try:
            with open("surf_history.txt", "r", encoding="utf-8", errors="replace") as file:
                history = file.read()
                print("\n--- SURF HISTORY LOG ---")
                print(history)
        except FileNotFoundError:
            print("Jarvis: No surf history found yet. Check the surf first!")
            
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