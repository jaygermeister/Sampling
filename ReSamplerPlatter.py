#-------------------------------------------------------------------------------
# Name:        PyReSampler Platter
# Purpose: This file takes in an mp3 or wav file as input, upsamples or downsamples the data, and then produces an output file in the same directory with a suffix that indicates the new bitrate
#
# Theory: The program uses the Pydub library to implement downsampling. When the user selects "downsampling" and enters a downsampling factor, Pydub applies a low-pass filter to the audio signal to remove 
# any high-frequency components beyond the new Nyquist frequency, and then decimates the signal by a factor equal to the downsampling factor. 
# This means that only every Nth sample is kept, where N is the downsampling factor. The resulting signal has a lower sampling rate and is effectively a downsampled version of the original signal.
# upsampling is achieved using linear interpolation. When upsampling, the program increases the number of samples in the audio data by a factor of factor. 
# For each new sample, the program calculates its amplitude by linearly interpolating between the two nearest original samples.
#
# Author:      Jayger
#
# Created:     13/05/2023
# Copyright:   (c) Jayger 2023
# Licence:     <License to Thrill>
#-------------------------------------------------------------------------------
import os
from tkinter import filedialog
from pydub import AudioSegment

# prompt the user to select the input file
input_file_path = ""
while not input_file_path.endswith((".wav", ".mp3")):
    input_file_path = filedialog.askopenfilename(title="Select input file", filetypes=(("Audio files", "*.wav;*.mp3"),))
    if not input_file_path:
        print("No input file selected. Exiting...")
        exit()

# print the original sample rate
audio = AudioSegment.from_file(input_file_path)
sample_rate = audio.frame_rate
print("Original sample rate:", sample_rate)

# prompt the user to input the resampling factor
factor_str = input("Enter the resampling factor (e.g. 2 for downsampling by 2, 0.5 for upsampling by 2): ")
try:
    factor = float(factor_str)
    if factor <= 0:
        raise ValueError("Resampling factor must be positive.")
except ValueError as e:
    print(f"Invalid resampling factor. {e} Exiting...")
    exit()

# resample the audio data
if factor >= 1:
    # downsampling
    resampled_audio = audio.set_frame_rate(int(sample_rate // factor))
else:
    # upsampling
    resampled_audio = audio.set_frame_rate(int(sample_rate * factor))

# construct output file path
input_file_dir, input_file_name = os.path.split(input_file_path)
output_file_path = os.path.join(input_file_dir, f"{os.path.splitext(input_file_name)[0]}_resampled_{int(resampled_audio.frame_rate)}{os.path.splitext(input_file_name)[1]}")

# write resampled audio data to output file
resampled_audio.export(output_file_path, format="wav")

print(f"Resampled file saved to {output_file_path}")
print(f"Resampled sample rate: {resampled_audio.frame_rate}")

# End
