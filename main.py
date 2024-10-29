from openai import OpenAI
from utils import record_audio, play_audio, load_memory, save_memory, update_memory, goodbye, get_response, get_transcription
import sys


ai_name = "Ava" # Sets the name of the AI 
not_goodbye = True
memory = load_memory() # Load the memory

while not_goodbye:
    
    client = OpenAI(
    organization='organization', # Replace with your own
    project='project link', # Replace with your own
    )

    record_audio('test.wav')
    audio_file = open('test.wav', "rb")
    
    # transcription = client.audio.transcriptions.create(
    #     model="whisper-1",
    #     file=audio_file
    # )
    user_input = get_transcription(client, audio_file)
    print(user_input)

    # Add to the memory
    update_memory(memory, "user", user_input)

    # Create the chat history based on the memory
    chat_history = [
        {"role": "system", "content": f"You are my {ai_name}. Please answer in short sentences"}
    ] + memory["conversations"]

    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=chat_history
    # )

    ai_response = get_response(client, chat_history)
    print(ai_response)
    
    # Add the AI responses to memory
    update_memory(memory, "assistant", ai_response)

    # Save the memory
    save_memory(memory)
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=ai_response
    )
    
    response.stream_to_file('output.mp3')
    play_audio('output.mp3')


    # Quit the program if the user says goodbye
    if goodbye(user_input):
        not_goodbye = False
        audio_file.close()
        sys.exit()