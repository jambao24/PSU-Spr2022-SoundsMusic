# Build filter coefficients for a half-band filter.
# Bart Massey 2020

from scipy import signal

# Build a Kaiser window filter with "optimal" length and
# "beta" for -40 dB of passband and stopband ripple and a
# 0.05 transition bandwidth. Prescale the coefficients to
# preserve the input amplitude.
nopt, bopt = signal.kaiserord(-40, 0.05)
subband = signal.firwin(nopt, 0.45, window=('kaiser', bopt), scale=True)

# Display the coefficients.
for s in subband:
    print(s)
