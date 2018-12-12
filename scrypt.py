#!/usr/bin/env
import os
import sys
from pathlib import Path
import argparse
# File til þess að sjá um scriptu

def main(args):
    directory = Path(args)
    for i in directory.glob('**/**/*.png'):
        print(i)

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Sort files')
    #parser.add_argument('Path', type=argparse., )
    try:
        directory = sys.argv[1]
        main(directory)
    except:
        print('something went wrong')
    