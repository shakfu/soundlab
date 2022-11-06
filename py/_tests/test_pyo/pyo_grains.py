import os
from pyo import *

HOME = os.environ['HOME']

s = Server().boot()
s.start()
snd = SndTable(f"{HOME}/Music/samples/s01.wav")
env = HannTable()
pos = Phasor(freq=snd.getRate()*.25, mul=snd.getSize())
dur = Noise(mul=.001, add=.1)
g = Granulator(snd, env, [1, 1.001], pos, dur, 32, mul=.1).out()

