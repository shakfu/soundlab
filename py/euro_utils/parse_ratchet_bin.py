"""shotkey: writes schottkey eurorack binary files

for each pattern of 32 patterns 
    12 tracks of 64 steps = 768 steps
    12 tracks of 64 ratchet steps =  768 rsteps
    12 tracks of 64 gate length steps where gate length 1 (trigger ) to 6 (tie to next step)
    12 tracks of 64 accents = 768 accents

search space = 4 * 768 * 32 patterns = 98,304

check: len(p) = 98,304


WIP (still proof-of-concept stage)

"""

import numpy as np

def get_file(path):
    with open(path, 'rb') as f:
        content = np.fromfile(f, dtype=np.ubyte)
    return content

edges = lambda: get_file('ratchet_edges.bin')
full = lambda: get_file('ratchet_full.bin')
p = get_file('ratchet_patterns.bin')

