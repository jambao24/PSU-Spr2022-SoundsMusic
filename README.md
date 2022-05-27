# PSU-Spr2022-SoundsMusic
repo for Spring 2022 CS510 (Music, Sound &amp; Computers) code

James Bao
HW 4 README


aleatoric.py is a Python program that plays continuous audio within a range of one octave from a specified root frequency according to a specified beat. This version proves proof of concept (it plays continuously) but doesn't handle user parameters, is written using PyAudio (has a lot of noise for some reason), and is played at double the tempo specified per the BPM. 

Default parameters-
•	--root KEYNUMBER: Use MIDI key number KEYNUMBER as the root tone of the scale. [72]
•	--beats SIG: Use a “time signature” of SIG beats per measure. [8]
•	--bpm BPM: Use a beat frequency of BPM beats per minute. [90.0]
•	--ramp FRAC: Use FRAC as a fraction of the beat time for the attack and release time for the note envelope. [0.5]
•	--accent VOLUME: Use the given VOLUME from 0..10 as the note volume for the first (accent) beat of each measure. [5.0]
•	--volume VOLUME: Use the given VOLUME from 0..10 as the note volume for the unaccented beats of each measure. [8.0]
 

(Note to self: aleatoric.py needs to be in the main GitHub repo folder to run properly due to how the venv is set up)