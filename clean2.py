##################
import os
from pathlib import Path
import re

season = re.compile('(S|s)[0-9][0-9]')
season_v2 = re.compile('Season [0-9][0-9]')
season_v3 = re.compile('[0-9]x[0-9][0-9]')

#find information about season /episode from a single file
def work_with_file(filename):
    ble = filename.replace('_', ' ').replace(".", " ")
    

#work with directories, check if they are already sorted or not
def work_with_dir(dirname):
    bla = dirname.replace('.', ' ')
    search_first_pattern = re.search('(S|s)[0-9][0-9]', dirname)
    if search_first_pattern:
        blee = search_first_pattern.group()
        print(blee)

def search(foldername):
    #using Path
    filepath = Path(foldername)
    some = list()
    
    directories = [x[0] for x in os.walk(filepath)]

    if '24' in directories:
        print(directories)

    return directories
        

#Búa til fall til þess að lesa metadata út úr hverjum file, nota regex til að gera það

print(search('downloads'))