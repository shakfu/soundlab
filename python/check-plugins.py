import os
import shutil
from pathlib import Path

HOME = os.environ['HOME']

VST = Path('/Library/Audio/Plug-Ins/VST')
VST3 = Path('/Library/Audio/Plug-Ins/VST3')
AU = Path('/Library/Audio/Plug-Ins/Components')


vsts = {i.stem for i in VST.iterdir()}
vst3s = {i.stem for i in VST.iterdir()}
aus = {i.stem for i in AU.iterdir()}



def get_duplicates_by_type(type='vst'):
    if type == 'vst':
        return sorted(list(aus.intersection(vsts)))
    elif type == 'vst3':
        return sorted(list(aus.intersection(vst3s)))
    else:
        print(f"Accepts 'vst' or 'vst3', '{type}' not implemented.")


def backup_duplicates_by_type(type='vst', dest_dir=HOME):
    print("Backup vsts which are duplicates of Audio Units")
    if type == 'vst':
        names = get_duplicates_by_type('vst')
        paths = [p for p in VST.iterdir() if p.stem in names]
        dest = Path(dest_dir) / 'Desktop' / 'VST_DUPS'
        try:
            os.makedirs(dest, exist_ok=True)
        except OSError:
            pass
        print(f"first creating backup to {dest}")
        for p in paths:
            shutil.copytree(p, dest / p.name)
        print("backup complete.")    


def remove_duplicates_by_type(type='vst', dest_dir=HOME):
    """removes vsts or vst3s which are the same as audio units"""
    print("REMOVE vsts which are duplicates of Audio Units (with backup)")
    if type == 'vst':
        names = get_duplicates_by_type('vst')
        paths = [p for p in VST.iterdir() if p.stem in names]
        for p in names:
            print(p)
        answer = input(f"Confirm removal of duplicate {type} plugins? (y/n) ")
        if answer == 'y':
            for p in paths:
                print(f'removing: {path.stem}')
                shutil.rmtree(p)
            print('removal complete')
        else:
            print('cancelled')

def get_plugins_by_brand(name, type='vst'):
    brand = Path(f'~/Downloads/music-tech/plugins/au-vst/{name}')
    ps = {i.stem for i in brand.iterdir()}

    _result = []
    if type == 'au':
        for i in ps.intersection(aus):
            target = AU / f'{i}.vst'
            _result.append(target)
    elif type == 'vst':
        for i in ps.intersection(vsts):
            target = VST / f'{i}.vst'
            _result.append(target)
    elif type == 'vst3':
        for i in ps.intersection(vst3s):
            target = VST / f'{i}.vst'
            _result.append(target)
    else:
        print(f"Accepts 'au' or 'vst' or 'vst3', '{type}' not implemented.")

    return _result

#remove_duplicates_by_type()
#backup_duplicates_by_type()
