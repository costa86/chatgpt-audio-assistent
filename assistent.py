from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import openai

FILE_NAME = "gpt"
text_file = f"{FILE_NAME}.txt"
audio_file = f"{FILE_NAME}.wav"


def get_file_content(file_name: str = text_file) -> str:
    with open(file_name, "r") as f:
        return f.read()


def call_chat_gpt(text_file: str = text_file, prompt: str = "What are you?"):
    openai.api_key = get_file_content("key.txt")

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    text = response["choices"][0]["text"]

    with open(text_file, "w") as f:
        f.write(text)


def save_audio_file(text: str, audio_file: str):
    tts = gTTS(text)
    tts.save(audio_file)


def get_mic_input(language: str = "en-us") -> str:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Say something!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language=language)
    return str(text)


def speak(text: str):
    save_audio_file(text, audio_file)
    playsound(audio_file)


speak("Hello. What would you like to ask ChatGPT?")
call_chat_gpt(prompt=get_mic_input())
speak(get_file_content())
