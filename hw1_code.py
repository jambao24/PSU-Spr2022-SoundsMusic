import numpy
from numpy import sin, pi
from scipy.io import wavfile
import matplotlib.pyplot as plt
import wave
import struct

# 48000 samples per second
# frequency = 440 Hz
sampleRate = 48000
freq = 440
length = 1

t = numpy.linspace(0, length, sampleRate * length)
amp = numpy.iinfo(numpy.int16).max
y = amp * numpy.sin(freq * 2 * numpy.pi * t)

'''
N = 109  # num samples in period
x = range(N)  # [0, 1, 2, ..., 108]
y = N * [0]  # [0,0,....,0]
for i in x:
    y[i] = 4 / pi * sin(2 * pi * i / N)
y = 440 * y  # 3 periods, y length is 3N
x = range(440 * N)  # [0, 1, 2, ..., 3*N-1]
'''

#x = numpy.range(sampleRate)
#plt.plot(x, y)
plt.plot(y)
plt.show()

# save y to 'sine.wav'
'''
fout = wave.open("sine.wav", "w")
fout.setnchannels(1)  # Mono
fout.setsampwidth(2)  # Sample is 2 bytes or 16 bits
fout.setframerate(48000)  # Sampling frequency
fout.setcomptype('NONE', 'Not Compressed')
BinStr = ""  # Create a binary string of data
for i in range(len(y)):
    BinStr = BinStr + struct.pack('h', round(y[i] * 20000))
fout.writeframesraw(BinStr)
fout.close()
'''

# https://dsp.stackexchange.com/questions/53125/write-a-440-hz-sine-wave-to-wav-file-using-python-and-scipy
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
wavfile.write('sine.wav', sampleRate, y.astype(numpy.int16))