import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import pyaudio
import sys

# https://realpython.com/python-command-line-arguments/
# https://stackoverflow.com/questions/49309446/python-wrong-number-of-arguments-exception
if not len(sys.argv) == 2:
    raise TypeError('my_code() takes either 2 or 3 arguments ({} given)'
                    .format(len(sys.argv) + 1))

inp_name = sys.argv[1]
out_name = "r" + inp_name

# predefined sample rates for working with the 3 test files
# 'gc.wav' has a input sample rate of 44100 samples/sec, the output sample rate (sRate_2) will be half that value
# 'sine.wav' and 'synth.wav' have a input sample rate of 48000 samples/sec
sampleRate1 = 48000
sRate_1 = 24000
sampleRate2 = 44100
sRate_2 = 22050

# load FIR filter coefficients
a_FIR = np.loadtxt('coeffs.txt')
N = len(a_FIR)

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# x_0 = input for convolution
x0 = np.zeros(N)
s_rate, x = wavfile.read(inp_name)
x_0 = np.append(x0, x)

# test case 1: check if gc.wav is being read in as the parameter [44100 samples/sec]
# 'output = True' indicates that the sound will be played rather than recorded
# (https://stackoverflow.com/questions/30684230/how-to-check-if-any-sys-argv-argument-equals-a-specific-string-in-python)
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sampleRate1,
                input=True,
                output=False)

# convolution: y is initially an empty array
y = np.zeros(len(x_0))
for i in range(N, len(x_0)):
    y0 = 0.0
    # https://stackoverflow.com/questions/4674473/valueerror-setting-an-array-element-with-a-sequence
    for j in range(N):
        a_val = a_FIR[j]
        b_val = x_0[i-j]
        y0 += a_val * b_val
    y[i] = y0

# decimate the convoluted signal, take every other element
y_out = y[::2]

# write the output at half the sampling rate of the input
if (s_rate == sampleRate2):
    write(out_name, sRate_2, y_out.astype(np.int16))
elif (s_rate == sampleRate1):
    write(out_name, sRate_1, y_out.astype(np.int16))

# Close and terminate the stream
stream.close()
p.terminate()