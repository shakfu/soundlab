import os
import shutil
from pathlib import Path

VST = Path('/Library/Audio/Plug-Ins/VST')
AU = Path('/Library/Audio/Plug-Ins/Components')


vsts = set(i.stem for i in VST.iterdir())
aus = set(i.stem for i in AU.iterdir())


def rm_puremagnetik_vsts():
    puremagnetik = Path('~/Downloads/music-tech/plugins/au-vst/puremagnetik')
    ps = set(i.stem for i in puremagnetik.iterdir())

    for i in ps.intersection(vsts):
        target = VST / f'{i}.vst'
        print(target)




