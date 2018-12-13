#!/usr/bin/env
import os
import sys
from pathlib import Path
import pathlib
import argparse
import re
import shutil
# File til þess að sjá um scriptu

def main(args):
    directory = Path(args)
    dirs_to_make = ['Images', 'Compressed Files', 'Movies', 'Shows']
    #for i in dirs_to_make:
    #    path_to_dir = os.path.join(args, i)
    #    if os.path.isdir(path_to_dir):
    #        continue
    #    else:
    #        os.mkdir(path_to_dir)
    to_find =['png','jpg']
    for a in to_find:
        path = '**/**/*.' + a
        for i in directory.glob(path):
            parent = os.path.dirname(i)
            new_path = os.path.join(dirs_to_make[0], i.name)

            try:
                shutil.move(i, new_path)
            except:
                pass
    zipped = ['zip', 'rar']
    for b in zipped:
        path = '**/**/*.' + b
        for i in directory.glob(path):
            new_path = os.path.join(dirs_to_make[0], i.name)
            print(new_path)
            #shutil.move(i, new_path)

if __name__ == '__main__':
    main('downloads')
#    try:
#        directory = sys.argv[1]
#        main(directory)
#    except:
#        print('something went wrong')
    