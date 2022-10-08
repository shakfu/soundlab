#!/usr/bin/env python3

import os
import glob
import shutil

CWD = os.getcwd()

projects = [p for p in os.listdir(CWD) if p.startswith('PROJECT')]

AUDIO = 'Audio'

for p in projects:
    wavs = glob.glob(f'{p}/*.wav')
    ot_files = glob.glob(f'{p}/*.ot')
    print(p, 'wavs:', wavs)
    print(p, 'ot_files:', ot_files)
    for wav in wavs:
        target = os.path.join(AUDIO, os.path.basename(wav))
        print('wav:', target)
        # shutil.copy(wav, target)
        shutil.move(wav, target)

    for ot_file in ot_files:
        target = os.path.join(AUDIO, os.path.basename(ot_file))
        print('ot:', target)
        # shutil.copy(wav, target)
        shutil.move(ot_file, target)

