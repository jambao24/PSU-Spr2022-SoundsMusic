import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write
import scipy.signal.windows as ssw
import scipy.fft as sf
import matplotlib.pyplot as plt
import pyaudio
import sys

# https://realpython.com/python-command-line-arguments/
# https://stackoverflow.com/questions/49309446/python-wrong-number-of-arguments-exception
if not len(sys.argv) == 2 and not len(sys.argv) == 1:
    raise TypeError('incorrect number of arguments (must include tuner.py)'
                    .format(len(sys.argv) + 1))

wavInput = False
liveInput = False
if len(sys.argv) == 2 and sys.argv[0].find("tuner.py") >= 0 and sys.argv[1].find(".wav") >= 0:
    wavInput = True
elif len(sys.argv) == 2 and sys.argv[0].find("tuner.py") >= 0:
    liveInput = True
# https://stackoverflow.com/questions/20844347/how-would-i-make-a-custom-error-message-in-python
if not wavInput and not liveInput:
    raise ValueError('Input must be a wav file (.wav) or tuner.py')


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
    n = (217*4)
    x_0 = x[10*n:11*n]
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.triang.html
    tri_window = ssw.triang(n)
    x_new = np.multiply(x_0, tri_window)

    # https://stackoverflow.com/questions/4364823/how-do-i-obtain-the-frequencies-of-each-value-in-an-fft?lq=1
    x_spec_output = sf.rfft(x_new)
    # print(abs(x_spec_output))
    # x_s_o = np.where(x_spec_output >= 0)
    x_so_mag = np.abs(x_spec_output) / n

    f_val = np.argmax(x_so_mag)
    print(f_val*s_rate/n, 'Hz')


if liveInput:
    # not added yet
    print("functionality coming soon!")