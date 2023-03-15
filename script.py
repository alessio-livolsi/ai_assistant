# Python
import concurrent.futures
import os
import requests

# Third Party
import speech_recognition as sr
import pyttsx3
from decouple import config


def main():
    # Set up OpenAI API credentials
    openaiurl = "https://api.openai.com/v1"
    openai_token = config("OPENAIKEY")

    # Exit the program if API key is not available
    if openai_token == "":
        os.exit(1)
    headers = {"Authorization": f"Bearer {openai_token}"}

    # Record audio from the user's microphone
    print("[-] Record audio using microphone")

    # Gather audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

    # Set up a folder and file name for storing the audio file
    folder = "./audio"
    filename = "microphone-results"
    audio_file_path = f"{folder}/{filename}.wav"

    # Create the audio folder if it does not exist
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Write the recorded audio to a WAV file
    print(f"Generating WAV file, saving at location: {audio_file_path}")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # execute the write to file operation in a separate thread
        future = executor.submit(
            write_audio_file, audio_file_path, audio.get_wav_data()
        )

        # Call the Whisper API to perform speech-to-text on the audio file
        print("[-] Call to Whisper API's to get the STT response")

        url = f"{openaiurl}/audio/transcriptions"

        data = {
            "model": "whisper-1",
            "file": audio_file_path,
        }
        files = {"file": open(audio_file_path, "rb")}

        # execute the HTTP request to the Whisper API in a separate thread
        future2 = executor.submit(
            requests.post, url, files=files, data=data, headers=headers
        )

        # wait for the HTTP request and write to file operations to complete
        response = future2.result()
        write_result = future.result()

    print("Status Code", response.status_code)
    speech_to_text = response.json()["text"]
    print("Response from Whisper API's", speech_to_text)

    # query ChatGPT model with text and generate a response

    print("[-] Querying ChatGPT model with the STT response data")
    url = f"{openaiurl}/chat/completions"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": speech_to_text,
            }
        ],
    }

    response = requests.post(url, json=data, headers=headers)

    print("Status Code", response.status_code)
    chatgpt_response = response.json()["choices"][0]["message"]["content"]
    print("Response from ChatGPT model ", chatgpt_response)

    # Convert TTS from the response

    print("[-] Try to convert TTS from the response")

    engine = pyttsx3.init()
    engine.setProperty("rate", 110)

    print("Converting text to speech...")
    engine.say(chatgpt_response)

    engine.runAndWait()
    engine.stop()


def write_audio_file(audio_file_path, audio_data):
    with open(audio_file_path, "wb") as f:
        f.write(audio_data)


if __name__ == "__main__":
    main()
