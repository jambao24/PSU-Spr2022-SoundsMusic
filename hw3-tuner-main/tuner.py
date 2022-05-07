import numpy as np
import struct
from scipy.io import wavfile
from scipy.io.wavfile import write
import scipy.signal.windows as ssw
import scipy.fft as sf
import matplotlib.pyplot as plt
import pyaudio
import sys

'''
simple function for finding the largest exponent of 2 within the bounds of
an array length arr_len
this function is only called with the parameters:
1) length of the wav file numpy array len(x)
2) initial value of n (2**17)
'''
def find_exponent_2(arr_len, val):
    if (val >= arr_len):
        return find_exponent_2(arr_len, val//2)
    else:
        return val


# https://realpython.com/python-command-line-arguments/
# https://stackoverflow.com/questions/49309446/python-wrong-number-of-arguments-exception
if not len(sys.argv) == 2 and not len(sys.argv) == 1:
    raise TypeError('incorrect number of arguments (must include tuner.py)'
                    .format(len(sys.argv) + 1))

wavInput = False
liveInput = False
if len(sys.argv) == 2 and sys.argv[0].find("tuner.py") >= 0 and sys.argv[1].find(".wav") >= 0:
    wavInput = True
elif len(sys.argv) == 1 and sys.argv[0].find("tuner.py") >= 0:
    liveInput = True
# https://stackoverflow.com/questions/20844347/how-would-i-make-a-custom-error-message-in-python
if not wavInput and not liveInput:
    raise ValueError('Input must contain tuner.py')


# Case 1: we are reading in a wav file
if wavInput:

    inp_name = sys.argv[1]
    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # audio data is read in as numpy array x
    s_rate, x = wavfile.read(inp_name)

    # 'output = True' indicates that the sound will be played rather than recorded
    # (https://stackoverflow.com/questions/30684230/how-to-check-if-any-sys-argv-argument-equals-a-specific-string-in-python)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=s_rate,
                    input=True,
                    output=False)



    # https://stackoverflow.com/questions/12332392/triangle-wave-shaped-array-in-python

    # take 1st n samples of input
    n = 2 ** 17
    # Case 1: input contains more than 2 ** 17 samples
    if (len(x) > n):
        x_0 = x[:n]
    # Case 2: input contains less than 2 ** 17 samples
    # we need to find the largest exponent of 2 that works
    else:
        n_0 = find_exponent_2(len(x), n)
        n = n_0
        x_0 = x[:n]

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.triang.html
    # create triangular window and multiply signal by window
    tri_window = ssw.triang(n)
    x_new = np.multiply(x_0, tri_window)

    # https://stackoverflow.com/questions/4364823/how-do-i-obtain-the-frequencies-of-each-value-in-an-fft?lq=1
    x_spec_output = sf.rfft(x_new)
    # print(abs(x_spec_output))
    # x_s_o = np.where(x_spec_output >= 0)
    x_so_mag = np.abs(x_spec_output) / (n)

    f_val = np.argmax(x_so_mag)
    # round highest magnitude frequency found to 1 decimal place
    print(np.round(f_val*s_rate/(n), 1), 'Hz')


# Case 2: we're reading in continuous input from the user's microphone
# https://www.codespeedy.com/get-voice-input-with-microphone-in-python-using-pyaudio-and-speechrecognition/
# https://www.youtube.com/watch?v=AShHJdSIxkY
if liveInput:
    ## not added yet
    #print("functionality coming soon!")

    # sampling rate = 48000 samples/s
    RATE = 48000
    CHUNK = 4096 # 2 ** 12

    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # 'output = True' indicates that the sound will be played rather than recorded
    # (https://stackoverflow.com/questions/30684230/how-to-check-if-any-sys-argv-argument-equals-a-specific-string-in-python)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        x_0 = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] + 127
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.triang.html
        # create triangular window and multiply signal by window
        tri_window = ssw.triang(len(x_0))
        x_new = np.multiply(x_0, tri_window)

        # https://stackoverflow.com/questions/4364823/how-do-i-obtain-the-frequencies-of-each-value-in-an-fft?lq=1
        x_spec_output = sf.rfft(x_new)
        # print(abs(x_spec_output))
        # x_s_o = np.where(x_spec_output >= 0)
        x_so_mag = np.abs(x_spec_output) / (len(x_0))

        f_val = np.argmax(x_so_mag)
        # round highest magnitude frequency found to 1 decimal place
        print(np.round(f_val * RATE / (len(x_0)), 1), 'Hz')

