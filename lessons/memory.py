import json
import os
def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as file:
            return json.load(file)  
    else:
        return {}
def save_memory(memory):
    with open("memory.json", "w") as file:
       json.dump(memory, file, indent = 4)