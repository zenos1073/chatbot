import pyttsx3
import requests
import wikipedia
import pyaudio
import os
import openai
import datetime
import speech_recognition as sr
import webbrowser
import subprocess
from api import api_key
import random

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)

chatStr=''


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def chat(query):
    global chatStr
    openai.api_key = api_key
    chatStr+=f"User: {query}\n Naira: "
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": chatStr
            }
        ]
    )
    speak(response['choices'][0]['message']['content'])
    chatStr+=f"{response['choices'][0]['message']['content']}\n"

    return response['choices'][0]['message']['content']


def ai(prompt):

    openai.api_key = api_key
    text=f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ]
    )
    generated_text = response["choices"][0]["message"]["content"]
    #print(generated_text)

    if not os.path.exists("result"):
        os.mkdir("result")

    file_path = f"result/{''.join(prompt.split('intelligence')[1:])}.txt"
    with open(file_path, "w") as f:
        f.write(generated_text)

    return generated_text


def get_weather(city):
    api_key = "60db880d03806a4a5903421aa2347e10"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # You can change this to 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['cod'] == '404':
        speak("Sorry, I couldn't find the weather information for that city.")
    else:
        try:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")
        except KeyError as e:
            print(f"Error: {e}. Full response: {data}")
            speak("Sorry, there was an issue retrieving the weather information.")


Names = ['naira', 'nayara', 'nyara', 'naera','noida']


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("good morning!")
    elif 12 <= hour < 18:
        speak("good afternoon!")
    else:
        speak("good evening!")

    speak("I am Naira, how may I help you? ")


def input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.0
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said:{query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query


def open_user(image_path):
    subprocess.Popen(["start", "", image_path], shell=True)


if __name__ == "__main__":
    #wishme()
    """query1 = input().lower()
    if any(name in query1 for name in Names):
        wishme()"""
    while True:
        sites = [['youtube', 'https://www.youtube.com'], ['google', 'https://www.google.com'],
                 ['instagram', 'https://www.instagram.com'], ['facebook', 'https://www.facebook.com'],
                 ['gmail', 'https://www.gmail.com']]
        query=input().lower()
        if query == "None":
            speak("I didn't hear anything. Goodbye!")
            break

        for site in sites:
            if f"Open {site[0]}".lower() in query:
                speak(f"Opening {site[0]}")
                webbrowser.open(site[1])

        if 'wikipedia' in query:
            speak("Searching wikipedia...")
            query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia")
            speak(results)

        elif 'weather in' in query:
            city = query.split("in")[1].strip()
            get_weather(city)

        elif 'camera' in query:
            speak("opening camera")
            path = r"C:\\Users\\jackw\\OneDrive\\Desktop\\Camera - Shortcut.lnk"
            subprocess.run(['start', '', path], shell=True)

        elif 'exit' in query:
            speak("Exiting...")
            exit()
        #elif 'your name' or 'who are you' in query:
            #speak("Hello! my name is Naira. How can i help you today?")

        elif 'whatsapp' in query:
            speak("opening whatsapp")
            path = r"C:\\Users\\jackw\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk"
            subprocess.run(['start', '', path], shell=True)

        elif 'spotify' in query:
            speak("opening spotify")
            path = r"C:\\Users\\jackw\\OneDrive\\Desktop\\Spotify - Shortcut.lnk"
            subprocess.run(['start', '', path], shell=True)

        elif 'using artificial intelligence' in query:
            ai(prompt=query)

        elif 'my photo' in query:
            speak("opening your photo")
            image_paths = r"C:\\Users\\jackw\\OneDrive\\Pictures\\Zenos\\IMG_4115.jpg"
            open_user(image_paths)

        elif 'telegram' in query:
            speak("opening telegram")
            path = r"C:\\Users\\jackw\\OneDrive\\Desktop\\Telegram Desktop - Shortcut.lnk"
            subprocess.run(['start', '', path], shell=True)

        elif 'command prompt' in query:
            speak("opening command prompt")
            path = r"C:\\Users\\jackw\\OneDrive\\Desktop\\Command Prompt - Shortcut.lnk"
            subprocess.run(['start', '', path], shell=True)

        elif 'created' in query:
            speak("Gonet created me. With the help of OpenAi.")

        elif 'netflix' in query:
            speak("opening netflix")
            path = r"C:\\Users\\jackw\\OneDrive\\Desktop\\Netflix - Shortcut.lnk"
            subprocess.run(['start', '', path], shell=True)

        elif 'motivation' in query:
            speak(
                "Embrace the challenges you encounter, for they are the stepping stones to success. Every effort you put in today brings you one step closer to your goals. Remember, the journey may be tough, but your determination and hard work will pave the way for your success. Keep pushing forward, stay focused, and believe in yourself—you've got this!")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'good night' in query:
            speak('goodnight sir!')

        elif 'good morning' in query:
            speak('good morning sir!')

        elif 'reset chat' in query:
            chatStr = ""

        else:
            chat(query)
