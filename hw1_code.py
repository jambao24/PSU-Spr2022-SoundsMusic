import numpy
from scipy.io import wavfile
import matplotlib.pyplot as plt
import wave

# 48000 samples per second
# frequency = 440 Hz
sampleRate = 48000
freq = 440
length = 1

t = numpy.linspace(0, length, sampleRate * length)
amp = numpy.iinfo(numpy.int16).max
y = amp * numpy.sin(freq * 2 * numpy.pi * t)

# x = numpy.range(sampleRate)
# plt.plot(x, y)
# plt.plot(y)
# plt.show()

# https://dsp.stackexchange.com/questions/53125/write-a-440-hz-sine-wave-to-wav-file-using-python-and-scipy
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
wavfile.write('sine.wav', sampleRate, y.astype(numpy.int16))

amp2 = amp * 0.5  # half the amplitude of the original value
y2 = amp2 * numpy.sin(freq * 2 * numpy.pi * t)
y2 = numpy.clip(y2, -0.5 * amp2, 0.5 * amp2)

# plt.plot(y2)
# plt.show()

wavfile.write('clipped.wav', sampleRate, y2.astype(numpy.int16))

# https://stackoverflow.com/questions/30675731/howto-stream-numpy-array-into-pyaudio-stream
import pyaudio

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sampleRate,
                output=True)

# Read data in chunks
data = y2.astype(numpy.int16).tobytes()

# Play the sound by writing the audio data to the stream
stream.write(data)

# Close and terminate the stream
stream.close()
p.terminate()
