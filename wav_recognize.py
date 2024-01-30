#!/usr/bin/env python3

import os
import sys
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(0)

MODEL_PATH = "model"

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{file_path}' in the current folder.")
        exit(1)

def check_audio_file(wave_file):
    if wave_file.getnchannels() != 1 or wave_file.getsampwidth() != 2 or wave_file.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)

def recognize_audio(model, recognizer, wave_file):
    while True:
        data = wave_file.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            print("r" + recognizer.Result().strip())
        else:
            print("p" + recognizer.PartialResult().strip())

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        exit(1)

    input_file = sys.argv[1]
    check_file_exists(MODEL_PATH)
    
    with wave.open(input_file, "rb") as wf:
        check_audio_file(wf)

        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(False)

        recognize_audio(model, recognizer, wf)

        print("f" + recognizer.FinalResult().strip())

if __name__ == "__main__":
    main()
