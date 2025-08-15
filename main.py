import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pygame
import os
from dotenv import load_dotenv
from gtts import gTTS
import os
from duckduckgo_search import DDGS
import threading

load_dotenv()
# Optional: custom music module
try:
    import music_library
except ImportError:
    music_library = None

newsapi = os.getenv("news_api")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize pygame mixer once
pygame.mixer.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        # Use gTTS with pygame, but non-blocking playback
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        # Don't block main thread; spawn a thread to wait for playback to finish & cleanup
        def wait_and_cleanup():
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            os.remove('temp.mp3')
        threading.Thread(target=wait_and_cleanup, daemon=True).start()
    except Exception as e:
        print(f"TTS error: {e}")
        speak_old(text)

def chat_with_llama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": prompt, "stream": False},
            timeout=5  # add timeout to avoid hanging
        )
        return response.json().get("response", "I'm not sure how to answer that.")
    except Exception as e:
        print(f"Ollama error: {e}")
        return None

# Create a persistent DDGS instance to reuse for faster searches
ddgs_instance = DDGS()

def live_search_response(query):
    try:
        results = list(ddgs_instance.text(query, region="wt-wt", safesearch="off", max_results=1))
        if results:
            return results[0]["body"]
        else:
            return "I couldn't find anything relevant."
    except Exception as e:
        print(f"DuckDuckGo error: {e}")
        return "Search failed due to an error."

def read_news():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}", timeout=5)
        if r.status_code == 200:
            articles = r.json().get("articles", [])
            if not articles:
                speak("Sorry, I could not find any news at the moment.")
                return
            news_summary = "Here are the top headlines. "
            for i, article in enumerate(articles[:5], 1):
                news_summary += f"Headline {i}: {article['title']}. "
            speak(news_summary)
        else:
            speak("Sorry, I was unable to fetch news.")
    except Exception as e:
        print(f"News error: {e}")
        speak("An error occurred while fetching news.")

def processcommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open twitter" in c:
        speak("Opening Twitter")
        webbrowser.open("https://twitter.com")

    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif c.startswith("play"):
        if music_library:
            song = c.split(" ", 1)[-1]
            music_library.play(song)
            speak(f"Playing {song}")
        else:
            speak("Music library module is not available.")

    elif "news" in c:
        read_news()

    elif "deactivate" in c:
        speak("Okay, deactivating now. Say hello to wake me up.")
        return "deactivate"

    else:
        response = chat_with_llama(c)
        if not response or "I don't know" in response:
            response = live_search_response(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing. Say hello to begin.")
    active = False

    while True:
        try:
            with sr.Microphone() as source:
                # Reduced ambient noise duration to 0.2s (quicker)
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print("Listening...")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)

            word = recognizer.recognize_google(audio)
            print(f"You said: {word}")

            if not active and "hello" in word.lower():
                speak("Yeah, I am here. What would you like me to do?")
                active = True

            elif active:
                result = processcommand(word)
                if result == "deactivate":
                    active = False

        except sr.WaitTimeoutError:
            print("Timeout. No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f"Could not reach Google's Speech service; {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")




 
