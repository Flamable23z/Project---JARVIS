import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)  # Speaking speed
    
    # Secret registry path to Microsoft George (UK Male)
    george_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
    
    try:
        engine.setProperty('voice', george_id)
    except Exception as e:
        print(f"Voice switch error: {e}")
        
    engine.say(text)
    engine.runAndWait()