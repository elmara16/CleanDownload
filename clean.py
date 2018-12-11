##################
import os
from pathlib import Path
import re
import fnmatch

season = re.compile('(S|s)[0-9][0-9]?')
season_v2 = re.compile('(S|s)eason [0-9]?[0-9]')
season_v3 = re.compile(' [0-9]?[0-9]x[0-9][0-9]')
season_v4 = re.compile(' [0-9][0-9][0-9]')
pirate_site = re.compile(' www.[A-Za-z]+.com ')

#find information about season /episode from a single file
def work_with_file(filename, dirname, dl_folder):
    new_path = work_with_dir(dirname, dl_folder)

    for i in filename:
        path_to_file = os.path.join(new_path, i) #move file to a new folder if possible
        if re.search(season_v2, dirname): #if already sorted, do nothing
            continue
        if new_path == dirname: #the path to file didn't change, ignore those
            ble = work_with_dir(i, dl_folder)
            lastguy = os.path.split(ble)[-1] #síðasti liðurinn í filename
            #checka hvort hann sé jafn heitinu á file
            if i == lastguy:
                print(path_to_file)
                new_filepath = path_to_file
            else:
                new_filepath = os.path.join(ble, i)
            #print(new_filepath)
                
        #einhverstaðar hér er kallað á gaurinn sem sér um að taka til og færa file á milli
        #cleanup = move_files(new_filepath, dirname)

#work with directories, check if they are already sorted or not
def work_with_dir(dirname, dl_folder):
    pirate = re.search(pirate_site, dirname)
    if pirate:
        somedir = dirname.replace('[', ' -').split(' - ')
        dirname = os.path.join(somedir[0], somedir[2])
    bla = dirname.replace('.', ' ').replace(' - ', ' ').replace('_', ' ').replace('[', '').replace(']', '')
    
    search_first_pattern = re.search(season, bla)
    search_2nd_pattern = re.search(season_v2, bla)
    search_3rd_pattern = re.search(season_v3, bla)
    search_pattern4 = re.search(season_v4, bla)
    new_dir = dirname
    season_output = ''
    if search_first_pattern: #S00E00
        blee = search_first_pattern.group()
        xx = bla.replace(blee, ',').split(',')[0]
        new_dir = xx.split('\\')[-1].strip().title()
        bleb = blee.replace(blee, 'Season ')
        season_output = bleb + str(int(blee[1:]))
        return os.path.join(dl_folder, new_dir, season_output)
    elif search_2nd_pattern: #Season xx
        season_output = search_2nd_pattern.group().title()
        dire = bla.replace(season_output, ',').replace('(', ',').split(',')[0]
        new_dir = dire.split('\\')[-1].strip().title()
        #print(new_dir, season_output)
        if new_dir == season_output: #ef season er new_dir á að ignora
            return dirname
        #season_output = search_string
        return os.path.join(dl_folder, new_dir, season_output)
        
    elif search_3rd_pattern: #00x00
        search_str = search_3rd_pattern.group()
        dire = bla.replace(search_str, ',').split(',')[0]
        new_dir = dire.split('\\')[-1].strip().title()
        bleb = search_str.replace(search_str[0], 'Season ') 
        season_output = bleb + str(int(search_str.split('x')[0])).strip()
        return os.path.join(dl_folder, new_dir, season_output)
    elif search_pattern4: #103 fyrsta er seria, seinni 2 eru þættir
        search_str = search_pattern4.group()
        bleb = search_str.replace(search_str[0], 'Season ')
        dire = bla.replace(search_str, ',').split(',')[0]
        season_output = bleb + search_str[1]
        new_dir = dire.split('\\')[-1].strip().title()
        return os.path.join(dl_folder, new_dir, season_output)
    else:
        return dirname #ignores file
    

def search(foldername):
    #using Path til að opna hana
    filepath = Path(foldername)
    some = list()
    # If using OS
    #fer í gegnum skránna
    for x, y, z in os.walk(filepath):
       
        #works with directory to check if the name
       # ble = Path(x)
       # print(ble)
        #print(work_with_dir(x, filepath))
        work_with_file(z, x, filepath)
    return some
        

#Búa til fall til þess að lesa, nota regex til að gera það

print(search('downloads'))