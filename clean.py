##################
import os
from pathlib import Path
import re

season = re.compile('(S|s)[0-9][0-9](E|e)[0-9][0-9]')
season_v2 = re.compile('Season [0-9][0-9]')
season_v3 = re.compile('[0-9]x[0-9][0-9]')

#find information about season /episode from a single file
def work_with_file(filename):
    ble = filename.replace('_', ' ').replace(".", " ")
    

#work with directories, check if they are already sorted or not
def work_with_dir(dirname, dl_folder):
    bla = dirname.replace('.', ' ').replace('-', '')
    search_first_pattern = re.search(season, bla)
    if search_first_pattern:
        blee = search_first_pattern.group()
        xx = bla.replace(blee, ',').split(',')
        newdir = xx[0].split('\\')[-1].title().strip()
        bleb = blee.replace(blee[0:], 'Season ')
        hoho = str(int(blee[1:3]))
        season_output = bleb + hoho
        new_path = os.path.join(dl_folder, newdir, season_output)
        print(new_path)

#til að taka alla fila í current folder og færa þá yfir í sorteraða folderið
def copy_files(old_path, new_path):
    pass

def search(foldername):
    #using Path til að opna hana
    filepath = Path(foldername)
    #some = list()
    # If using OS
    #counter = 0
    #fer í gegnum
    for x, y, z in os.walk(filepath):
        #some.append([x,y,z])
        #if counter == 1:
        #    break
        #counter += 1
        #works with directory to check if the name
        work_with_dir(x, filepath)
        #elif z.isfile():
        #   pass #do stuff
        

#Búa til fall til þess að lesa, nota regex til að gera það

search('downloads')