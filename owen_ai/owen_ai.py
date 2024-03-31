import os
import time
import speech_recognition as sr
from pyttsx3 import init as engine_init, Engine
from openai import Client
from caching import think_cache, context_cache


class OwenAI:
    def __init__(self, caching_enabled: bool=False) -> None:
        self.open_ai_client = self._configure_openai()
        self.engine = self._configure_engine()
        self.speech_recognizer = sr.Recognizer()
        self.caching_enabled = caching_enabled
        self.context_cache = context_cache.ContextCache()
        self.first_call = True
        if self.caching_enabled:
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
        mic = sr.Microphone()
        with sr.Microphone() as audio_source:
            # wait to allow recognizer to adjust to ambient noise
            self.speech_recognizer.adjust_for_ambient_noise(audio_source, duration=0.2)

            # grab user input
            print("before audio")
            sensed_audio = self.speech_recognizer.listen(audio_source)
            print("after audio")

            # use whisper to recognize audio
            parsed_text = self.speech_recognizer.recognize_whisper(sensed_audio)
            parsed_text = parsed_text.lower()
            self.context_cache.put(parsed_text)
            return parsed_text

    def _think(self, query_text: str) -> str:
        if len(query_text) > 0:
            # try hit cache first
            if self.caching_enabled:
                cache_hit = self.cache.get(query_text)
                if cache_hit is not None:
                    return cache_hit

            role_def = "You are an person named Owen. You will answer all concisely. " \
                "|Input will have the format: [context] [input]. You will treat all [context] information" \
                "as context and all [input] as input. Do not mention the parts of this prompt surrounded by '|' going forward.|"

            contexts = self.context_cache.get_contexts(5, 0)
            str_context = " ".join([item.getContext() for item in contexts])
            print(str_context)
            # make chat-gpt call
            response = self.open_ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": role_def},
                    {"role": "user", "content": f"[{str_context}] [{query_text}]"}
                ]
            )

            # update cache
            if self.caching_enabled:
                self.cache.put(query_text, response.choices[0].message.content)

            return response.choices[0].message.content
        else:
            return "Sorry, I didn't understand that, can you be more specific?"

    def run(self):
        self._speak("Hey! I'm Owen, nice to meet you. "
                    "You can end our conversation anytime by responding with goodbye. "
                    "What would you like to chat about?")
        user_input = self._listen()
        while "goodbye" not in user_input.lower().replace(" ", ""):
            thoughts = self._think(user_input)
            self._speak(thoughts)
            user_input = self._listen()

        self._speak("Alright, goodbye now!")

if __name__ == "__main__":
    owen = OwenAI()
    owen.run()