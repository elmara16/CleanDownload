##################
from os import *
from pathlib import Path
import re

def search(foldername):
    #using Path
    filepath = Path(foldername)
    some = set()
    for i in filepath.glob('downloads/**/*.*'):
        some.add(i)        
    return some

    # If using OS
    # counter = 0

    #for x, y, z in walk(filepath):
    #    print(x, y, z)
    #    counter += 1
    #    if counter == 2:
    #        break
        

#Búa til fall til þess að lesa metadata út úr hverjum file, nota regex til að gera það

search('downloads')