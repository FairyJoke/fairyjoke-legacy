#!/usr/bin/env python

from typing import List
from pathlib import Path


PATHS = ['./app/models', './app/db/mixins']
SPLITS = [' ', ',', '(', ')', ':']
MODEL_CLASS = 'db.Base'

def split_all(s:str) -> List[str]:
    for sep in SPLITS:
        s = s.replace(sep, ' ')
    return s.split(' ')

if __name__ == '__main__':
    for path in PATHS:
        path = Path(path)
        target = path / '__init__.py'
        with target.open('w') as f:
            print('Generating', target)
            for file in path.glob('./*.py'):
                print('Scanning file', file)
                module = file.stem
                classes = []
                for line in file.read_text().splitlines():
                    words = split_all(line)
                    # if not MODEL_CLASS in words:
                    #     continue
                    if not 'class' in words or words[0] != 'class':
                        continue
                    class_index = words.index('class')
                    class_name = words[class_index + 1]
                    print('Found class', class_name)
                    classes.append(class_name)
                if not classes:
                    continue
                print(f'from .{module} import {", ".join(classes)}', file=f)
