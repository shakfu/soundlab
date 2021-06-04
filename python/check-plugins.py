import os
import shutil
from pathlib import Path

HOME = Path(os.environ['HOME'])

VST = Path('/Library/Audio/Plug-Ins/VST')
VST3 = Path('/Library/Audio/Plug-Ins/VST3')
AU = Path('/Library/Audio/Plug-Ins/Components')


vsts = {i.stem for i in VST.iterdir()}
vst3s = {i.stem for i in VST3.iterdir()}
aus = {i.stem for i in AU.iterdir()}



def get_duplicates_by_type(plugintype='vst'):
    if plugintype == 'vst':
        return sorted(list(aus.intersection(vsts)))
    elif plugintype == 'vst3':
        return sorted(list(aus.intersection(vst3s)))
    else:
        print(f"Accepts 'vst' or 'vst3', '{plugintype}' not implemented.")


def backup_duplicates_by_type(plugintype='vst', dest_dir=HOME):
    print("Backup vsts which are duplicates of Audio Units")
    assert plugintype in ['vst', 'vst3']
    d = {'vst': VST, 'vst3': VST3}
    names = get_duplicates_by_type(plugintype)
    paths = [p for p in d[plugintype].iterdir() if p.stem in names]
    dirname = f'{plugintype.upper()}_DUPS'
    dest = Path(dest_dir) / 'Downloads' / dirname
    try:
        os.makedirs(dest, exist_ok=True)
    except OSError:
        pass
    print(f"first creating backup to {dest}")
    for p in paths:
        shutil.copytree(p, dest / p.name)
    print("backup complete.") 


def remove_duplicates_by_type_and_brand(brand, plugintype='vst', dest_dir=HOME):
    """removes vsts or vst3s which are the same as audio units"""
    print("REMOVE vsts which are duplicates of Audio Units")
    if plugintype == 'vst':
        names = set(get_duplicates_by_type('vst'))
        brand_dir = HOME / f'Downloads/music-tech/plugins/au-vst/{brand}'
        brand_names = set({i.stem for i in brand_dir.iterdir()})
        target_names = names.intersection(brand_names)
        print(names)
        print(brand_names)
        paths = [p for p in VST.iterdir() if p.stem in target_names]
        for p in target_names:
            print(p)
        # answer = input(f"Confirm removal of duplicate {plugintype} plugins? (y/n) ")
        # if answer == 'y':
        #     for p in paths:
        #         print(f'removing: {path.stem}')
        #         shutil.rmtree(p)
        #     print('removal complete')
        # else:
        #     print('cancelled')


def remove_duplicates_by_type(plugintype='vst', dest_dir=HOME):
    """removes vsts or vst3s which are the same as audio units"""
    print("REMOVE vsts which are duplicates of Audio Units")
    assert plugintype in ['vst', 'vst3']
    d = {'vst': VST, 'vst3': VST3}
    names = get_duplicates_by_type(plugintype)
    paths = [p for p in d[plugintype].iterdir() if p.stem in names]
    for p in names:
        print(p)
    answer = input(f"Confirm removal of duplicate {plugintype} plugins? (y/n) ")
    if answer == 'y':
        for p in paths:
            print(f'removing: {p.stem}')
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

#backup_duplicates_by_type('vst3')
#remove_duplicates_by_type('vst3')
# for b in ['puremagnetik', 'klevgrand']:
#     remove_duplicates_by_type_and_brand(b, type='vst', dest_dir=HOME)
