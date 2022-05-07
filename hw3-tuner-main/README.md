# PSU-Spr2022-SoundsMusic
repo for Spring 2022 CS510 (Music, Sound &amp; Computers) code

James Bao
HW 3 README


tuner.py is a Python program that returns the loudest frequency within a segment of an audio sample. It requires the numpy, struct, and scipy.io libraries to run. It accepts 1 input wav file as an input that is specified when the program is run in the command line using the following command: python tuner.py <wav file name>. 

The program can also be run with no wav file as a parameter: python tuner.py, in which case the program will print the loudest frequency of the audio coming from the microphone on said device. It will print a new frequency value for every 8192 samples while audio is being read in at a 48000 samples/s rate. (This doesn't always work when trying to play audio files from my laptop, but it works if there's an external audio source being played from a phone or from the user's voice).

If there is more than 1 argument (or no additional argument) after the file name, there will be an error message 

(Note to self: tuner.py needs to be in the main GitHub repo folder to run properly due to how the venv is set up)