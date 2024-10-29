import speech_recognition as sr
import pygame
import time
import os
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()

def record_audio(file_path):
    # Use the audio file as the audio source 
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        # Read the audio file
        audio_data = recognizer.listen(source) 
        print("Recording complete.")
        

        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data.get_wav_data())


def play_audio(file_path):
    # Starts the mixer
    pygame.mixer.init()
    # Loads the audio file
    pygame.mixer.music.load(file_path)
    # Sets the audio volume
    pygame.mixer.music.set_volume(0.7)
    # Plays the audio
    pygame.mixer.music.play()
    #Wait until the audio is finished playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)                             


MEMORY_FILE = 'memory.json'
def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"conversations": []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(memory, file)

def update_memory(memory, role, content):
    memory["conversations"].append({"role": role, "content": content})
    save_memory(memory)

def goodbye(user_input):
    return any(phrase in user_input.lower() for phrase in ["goodbye", "bye", "see you later"])

def get_transcription(client, audio_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text

def get_response(client, chat_history):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )
    return response.choices[0].message.content
