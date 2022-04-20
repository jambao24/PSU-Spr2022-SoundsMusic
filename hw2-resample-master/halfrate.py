import numpy
from scipy.io import wavfile
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





