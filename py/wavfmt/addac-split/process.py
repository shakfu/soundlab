#!/usr/bin/env python3

import os
import shutil
import string


# sox piano.wav -b 16 out.wav channels 1 rate 22050
# sox out.wav s.wav trim 0 10 : newfile : restart

letters = list(string.ascii_lowercase)
digits = list(string.digits)

double_letters = [f'{x}{y}' for x,y in zip(letters, letters)]
double_digits = [f'{x}{y}' for x,y in zip(digits, digits)]

search_space = letters + digits + double_letters + double_digits

src_files = list(sorted(os.listdir('src')))
src_paths = [os.path.join('src', f) for f in src_files]

dst_files = [f'{x}.wav' for x in search_space]
dst_paths = [os.path.join('dst', f) for f in dst_files]

for i, src in enumerate(src_paths):
    print(src, '->', dst_paths[i])
    shutil.copy(src, dst_paths[i])