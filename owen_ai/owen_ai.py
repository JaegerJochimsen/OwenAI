import os
import speech_recognition as sr
from pyttsx3 import init as engine_init, Engine
from openai import OpenAI, Client
from caching import think_cache


class OwenAI:
    def __init__(self) -> None:
        self.open_ai_client = self._configure_openai()
        self.engine = self._configure_engine()
        self.speech_recognizer = sr.Recognizer()
        # fixme improve package for imports
        self.cache = think_cache.ThinkCache()

    def _configure_openai(self):
        os.environ["OPENAI_API_KEY"] = input("Enter your OpenAI API key: ").strip()
        return Client(api_key=os.environ["OPENAI_API_KEY"])

    def _configure_engine(self) -> Engine:
        engine = engine_init()
        engine.setProperty('rate', 180)
        engine.setProperty('voice', engine.getProperty('voices')[14].id) # use Daniel's voice for Owen
        return engine

    def _speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()
        return

    def _listen(self) -> str:
        with sr.Microphone() as audio_source:
            # wait to allow recognizer to adjust to ambient noise
            self.speech_recognizer.adjust_for_ambient_noise(audio_source, duration=0.2)

            # grab user input
            sensed_audio = self.speech_recognizer.listen(audio_source)

            # use whisper to recognize audio
            parsed_text = self.speech_recognizer.recognize_whisper(sensed_audio)
            parsed_text.lower()
            return parsed_text

    def _think(self, text: str) -> str:
        if len(text) > 0:
            # try hit cache first
            cache_hit = self.cache.get(text)
            if cache_hit is not None:
                return cache_hit

            # make chat-gpt call
            response = self.open_ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an enthusiastic AI assistant named OwenAI or Owen for short"},
                    {"role": "user", "content": text}
                ]
            )

            # update cache
            self.cache.put(text, response.choices[0].message.content)

            self._speak(response.choices[0].message.content)
        else:
            return "Sorry, I didn't understand"


    def run(self):
        self._speak("Hey! I'm Owen, nice to meet you. I am your AI assistant. What would you like to know?")
        self._think(self._listen())
