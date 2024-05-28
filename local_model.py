from datetime import datetime

from pydub import AudioSegment
from transformers import pipeline
import os


def add_to_path(directory):
    # Get the current PATH
    current_path = os.environ.get('PATH', '')

    # Check if the directory is already in PATH
    if directory not in current_path.split(os.pathsep):
        # Append the directory to PATH
        updated_path = current_path + os.pathsep + directory

        # Set the new PATH
        os.environ['PATH'] = updated_path
        print(f"Directory {directory} added to PATH for the current session.")
    else:
        print("Directory is already in the PATH.")


def m4a_to_wav(m4a_file, output_path):
    audio = AudioSegment.from_file(m4a_file, format="m4a")
    output_file = os.path.splitext(output_path)[0] + ".wav"
    audio.export(output_file, format="wav")


# Example usage
directory_to_add = r'C:\Users\Misha\Desktop\ffmpeg-4.2.1-win64-shared\bin'
add_to_path(directory_to_add)

# # Provide the input m4a file path and desired output wav file path
# m4a_file = "./dad.m4a"
# output_wav_file = "./dad.wav"
#
# # Convert m4a to wav
# m4a_to_wav(m4a_file, output_wav_file)

before = datetime.now()
pipe = pipeline("automatic-speech-recognition",
                r"C:\Users\Misha\Desktop\whisper-large-v2",
                )  # if you don't have GPU, remove this argument
file = "load model from files"
x = 100 - len(file)
after = datetime.now()
print(file, " " * x, ' ==>', before, after, after - before)

file = "carol.wav"
dad_transcription = pipe(file,
                         chunk_length_s=30,
                         stride_length_s=5,
                         batch_size=8, return_timestamps=True)

after = datetime.now()
x = 100 - len(file)
print(file, " " * x, ' ==>', before, after, after - before)

print("text format: ")
print(dad_transcription["text"])

print("============================")
print("chunk format: ")
for line in dad_transcription["chunks"]:
    print(line)
