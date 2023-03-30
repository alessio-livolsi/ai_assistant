# AI Assistant

## Overview

This script allows you to utilize OpenAI's ChatGPT and Whisper APIs in Python to integrate several AI services, 
including speech-to-text (STT), natural language processing (NLP).  

## Get Started
- Download or clone the repo
- Head over to OpenAI, make an account and generate an API Key > https://bit.ly/3Lo0TRn
- Be sure to store the API key in an environment variable
- Set up a virtual environment and `pip install -r requirements.txt`
- To run the script `python script.py`
- You shall be prompted to speak into your microphone and `Say something!`
- The script will generate a WAV file and save at ./audio/microphone-results.wav
- Then a Call to Whisper API's to get the STT response
- The script uses pyttsx3 package to covert the response and plays it back through the user's speakers

## Prerequisites
- I'm running MacOS Ventura 13.1 and to ensure the audio worked install `brew install portaudio`


## Enjoy 🙃
