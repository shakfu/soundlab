#!/usr/bin/env python3

import os
from pathlib import Path


for p in sorted(os.listdir('src')):
    p = Path(p)
    os.system(f"./bin/vultc -ccode -template pd src/{p} -o cpp/{p.stem}")
