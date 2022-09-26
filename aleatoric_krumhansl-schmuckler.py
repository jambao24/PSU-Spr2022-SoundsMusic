import math

import numpy as np
import random
import struct
from scipy.io import wavfile
from scipy.io.wavfile import write
import scipy.signal.windows as ssw
import scipy.fft as sf
import matplotlib.pyplot as plt
import pyaudio
import sounddevice as sd
import sys
import argparse


# default parameter values if none are given

# root
KEYNUMBER = 48
# beat (time signature)
SIG = 8
# beats per min
BPM = 90.0
# ramp (for note envelope)
FRAC = 0.5
# vol of accented beat
VOL1 = 5.0
# vol of unaccented beat
VOL0 = 8.0

# https://www.youtube.com/watch?v=cdblJqEUDNo
# https://docs.python.org/3/howto/argparse.html
# parse (optional) agruments
parser = argparse.ArgumentParser()
parser.add_argument("--root", type=int, help="MIDI key number as the root tone of the scale")
parser.add_argument("--beats", type=int, help="time signature of SIG beats per measure")
parser.add_argument("--bpm", type=float, help="beat frequency of BPM")
parser.add_argument("--ramp", type=float, help="fraction of the beat time for the attack and release time for the note envelope (0 to 0.5)")
parser.add_argument("--accent", type=float, help="note volume for the first (accent) beat of each measure (0 to 10)")
parser.add_argument("--volume", type=float, help="note volume for the unaccented beats of each measure (0 to 10)")
args = parser.parse_args()

# modify default parameters based on command line argument input
if args.root and args.root > 116:
    KEYNUMBER = 116
if args.root:
    KEYNUMBER = args.root
if args.beats:
    SIG = args.beats
if args.bpm:
    BPM = args.bpm
if args.ramp and args.ramp <= 0.0:
    FRAC = 0.0
if args.ramp and args.ramp > 0.5:
    FRAC = 0.5
if args.accent and args.accent < 0.0:
    VOL1 = 0.0
if args.accent and args.accent > 0.0:
    VOL1 = 10.0
if args.volume and args.volume < 0.0:
    VOL0 = 0.0
if args.volume and args.volume > 10.0:
    VOL0 = 10.0




# calculate the frequency of a wave for a given MIDI key number
def freq_MIDI(k):
    val = (k - 69) / 12
    return 440 * (2.0 ** val)


# https://stackoverflow.com/questions/11604653/how-to-add-command-line-arguments-with-flags-in-python3
# https://realpython.com/python-command-line-arguments/
# evidently I don't understand Python command line argument flags

# major scale (e.g. C D E F G A B C) describing how many tones above the root we want to generate notes for
major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
minor_scale = [0, 2, 3, 5, 7, 8, 10, 12]

# get Krumhansl-Schmuckler values
major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
# normalize the K-S values to compute probabilties (edit: maybe don't do this, we don't want the probability of any one note occuring to be 0)
major_profile_ = major_profile
#major_profile_ -= np.min(major_profile)
minor_profile_ = minor_profile
#minor_profile_ -= np.min(minor_profile)
# compute probability of each note occurring, need to adjust for 'do' one octave higher than the base frequency
major_profile_probs = np.divide(major_profile_, np.sum(major_profile_)+major_profile_[0])
#print(major_profile_probs)
minor_profile_probs = np.divide(minor_profile_, np.sum(minor_profile_)+minor_profile_[0])
#print(minor_profile_probs)

# create weighted 12-tone scale with major profile probabilities
major_scale_weighted = np.zeros(1000)
minor_scale_weighted = np.zeros(1000)
i = 0
h = 0
for j in range(0, major_profile_probs.size):
    tempval1 = math.floor(major_profile_probs[j] * 1000)
    tempval2 = math.floor(minor_profile_probs[j] * 1000)
    major_scale_weighted[i: i+tempval1] = j
    minor_scale_weighted[h: h + tempval2] = j
    i += tempval1
    h += tempval2
# add probabilistic values for 'do' at one octave higher
major_scale_weighted[i:1000] = major_profile_probs.size
minor_scale_weighted[h:1000] = minor_profile_probs.size

# https://www.statology.org/python-numpy-array-to-list/
major_scale_w = major_scale_weighted.tolist()
print(major_scale_w)
minor_scale_w = minor_scale_weighted.tolist()

# determine and get the frequency of one (non)randomly generated note
# uses either the weighted major scale or the weighted minor scale
def get_note_freq():
    MIDI_val = major_scale_w[random.randint(0, 1000)] + KEYNUMBER
    #MIDI_val = minor_scale_w[random.randint(0, 11)] + KEYNUMBER
    fr = freq_MIDI(MIDI_val)
    return fr


# generate a sequence of random MIDI numbers for a sequence of notes
# MIDI_vals = [major_scale[random.randint(0, 8) + KEYNUMBER] for i in range(0, 9000)]



# https://stackoverflow.com/questions/21146540/trapezoidal-rule-in-python


# sampling rate = 48000 samples/s
RATE = 48000
# determine number of samples in each beat to be generated, but as an int value
beat_chunk = round(RATE * 60 / BPM)

## Create an interface to PortAudio
#p = pyaudio.PyAudio()

# Create sounddevice interface?

# 'output = True' indicates that the sound will be played rather than recorded
# (https://stackoverflow.com/questions/30684230/how-to-check-if-any-sys-argv-argument-equals-a-specific-string-in-python)
stream = sd.RawOutputStream(
    samplerate=RATE,
    blocksize=beat_chunk,
    channels=1,
    dtype='int16',
)

# keep track of the beat number
beat = 0

y_out = np.linspace(0, 0, beat_chunk)

while (True):
    # create sine wave for the current beat
    # get_note_freq() generates a random frequency based on the given KEYNUMBER
    t = np.linspace(0, 60/BPM, beat_chunk)
    #amp = np.iinfo(np.int16).max
    f = get_note_freq()

    # generate square wave if accented beat
    if beat % SIG == 0:
        y = 4 * np.floor(f * t) - 2 * np.floor(2 * f * t) + 1
    # generate sine wave if unaccented beat
    else:
        y = np.sin(2 * np.pi * f * t)
        #y = 8 * np.floor(f * t) - 4 * np.floor(2 * f * t) + 1

    # apply the window to the beat...

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.triang.html
    # if FRAC >= 0.5, we create triangular window and multiply signal by window
    #if FRAC >= 0.5:
    #    window = ssw.triang(beat_chunk)
    # we need to use FRAC to generate our own trapezoidal window :(
    window = np.ones(beat_chunk)
    max1 = round(beat_chunk * FRAC)
    max2 = beat_chunk - max1
    # use np.linspace to increment the window up/down from 0/1 to 1/0
    window[0:max1] = np.linspace(0, 1, max1)
    window[max2:beat_chunk] = np.linspace(1, 0, max1)

    y_new = np.multiply(window, y)

    if beat % SIG == 0:
        y_new *= (10 ** (-6*(10-VOL1)/20))
    else:
        y_new *= (10 ** (-6*(10-VOL0)/20))


    # append to output wav file
    y_out = np.append(y_out, y_new)

    sd.wait()
    sd.play(y_new, RATE)

    # update the beat number
    beat += 1

    #write('sample_output.wav', RATE, y_out.astype(np.int16))


stream.close()