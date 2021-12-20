#!/usr/bin/env python3

from pathlib import Path
import os
import sys

sys.path.append(str(Path('.').resolve()))

if __name__ == '__main__':
    thumbnails_folder = Path(sys.argv[1]).absolute()
    target = Path(sys.argv[2]).absolute()

    target.mkdir(parents=True, exist_ok=True)
    os.chdir(target)
    for file in thumbnails_folder.glob('./*.arc'):
        os.system(f'arcutils {file}')
    output = target / 'data' / 'jacket' / 'thumbnail'
    for file in output.glob('./*.dds'):
        dest = Path(target / file.name).with_suffix('.jpg')
        os.system(f'convert -verbose {file} {dest}')
        file.unlink()
    os.system(f'rmdir -p -v {target / "data"}')
