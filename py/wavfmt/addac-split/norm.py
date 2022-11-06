import os

def norm(s, without_prefix=''):
    return '_'.join(
        s.lower().\
        replace('-','').\
        replace('#','s').\
        replace('_bpm', '').\
        lstrip(without_prefix).\
        split()
    )

files = os.listdir('.')

for i, name in enumerate(files):
    toname = f"{i:02}_{norm(name, 'atmosphere')}"
    os.rename(name, toname)
