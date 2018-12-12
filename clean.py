##################
import os
from pathlib import Path
import re
import fnmatch
import shutil
from itertools import cycle
import urllib
from urllib.request import urlopen
import json
from os import listdir
from os.path import isfile, join

season = re.compile('(S|s)[0-9][0-9]?')
season_v2 = re.compile('(S|s)eason [0-9]?[0-9]')
season_v3 = re.compile(' [0-9]?[0-9]x[0-9][0-9]')
season_v4 = re.compile(' [0-9][0-9][0-9]')
pirate_site = re.compile(' www.[A-Za-z]+.com ')

#Tætar í sig files og folders
def regexclean(line):
    line = line.split('\\')[-1].title().strip()
    line = re.sub(r'\[[^()]*\]', '', line)
    line = re.sub(r'\([^()]*\)', '', line)
    line1 = re.search('([^\\\]+)\.(avi|mkv|mpeg|mpg|mov|mp4|)$', line)
    if line1:
        line = line1.group(1)
    line = line.replace('.', ' ').lower()
    line2 = re.search('(.*?)(srt|mp4|mp3|avi$|dvdrip|hd|xvid|hdtv|dvdscr|brrip|divx|[\{\(\[]?[0-9]{4}).*', line)
    if line2:
        line = line2.group(1)
    # remove resolation
    line3 = re.search('(.*?)(blueray|240p|360p|480p|720p|1080p|[\{\(\[]?[0-9]{4}).*', line)
    if line3:
        line = line3.group(1)
    line = line.strip()
    # remove season
    line4 = re.search('(.*?)([a-z],|[0-9] sería|seria [0-9]|[0-9]{3}|s[0-9]|e[0-9]|[0-9],|[0-9]{2}x[0-9]{2}|[0-9]-[0-9]|s[0-9]{2}|seasons|season|s[0-9]{2}[e][0-9]{2}|[\{\(\[]?[0-9]{4}).*', line)
    if line4:
        line = line4.group(1)
    # annad rusl
    line4 = re.search('(.*?)(ice$|the complete$|torrent$|uk$|us$|ísl|®|[\{\(\[]?[0-9]{4}).*', line)
    if line4:
        line = line4.group(1)
    line = re.sub(r'^s[0-9]{2}e[0-9]{2}', '',line)
    line = line.replace('-', ' ')
    line = line.replace("'", '')
    line = line.replace("_", '')
    line = line.replace("", '')
    line = re.sub(r'\([^()]*\)', '', line)
    line = re.sub(' +',' ',line)
    line = line.strip()
    return line
    
def gettype(title):
    try:
        url = 'http://www.omdbapi.com/?apikey=852159f0&t='+title
        ble = urlopen(url)
        json_data = json.loads(ble.read())
        return(json_data['Type'])
    except:
        return("None")
#gettype("how%20i%20met%20your%20mother")

# Moves folders and files
def moveFiles(pathTocurrentFile, pathToNewDestination):
    shutil.move(pathTocurrentFile, pathToNewDestination)

#working with only folder þ.e paths
def driverFolders(filepath):
    count = 0
    count2 = 0
    done = False
    directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == 1]
    count2 = directories.count(directories[-1])
    licycle = cycle(directories)
    needUpdate = False
    while(done == False):
        if needUpdate == True:
            directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == 1]
            count2 = directories.count(directories[-1])
            licycle = cycle(directories)
            needUpdate = False
        x = next(licycle)
        if x == directories[-1]:
            count += 1
            if count == count2:
                done = True
        Rex = regexclean(x)
        dirName = filepath/Rex

        if not os.path.exists(dirName):
            Path.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
        try:
            moveFiles(x, filepath/Rex)
            print("Moved ", x)
        except:
            pass

#working on files after folders have been workt on     
def driverFilesOnly(filepath):
    onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    count = 0
    count2 = 0
    done = False
    count2 = onlyfiles.count(onlyfiles[-1])
    licycle = cycle(onlyfiles)
    needUpdate = False
    print(onlyfiles[-1])
    while(done == False):
        if needUpdate == True:
            onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
            count2 = onlyfiles.count(onlyfiles[-1])
            licycle = cycle(onlyfiles)
            needUpdate = False
        x = next(licycle)
        if x == onlyfiles[-1]:
            count += 1
            if count == count2:
                done = True
        Rex = regexclean(x)
        dirName = filepath/Rex
        dirFile = "downloads\\" + x

        if not os.path.exists(dirName):
            Path.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
        try:
            moveFiles(dirFile, filepath/Rex)
            print("Moved ", dirFile)
        except:
            pass

#setja folder sem meika ekki sense fyrir movies eda series i aðra folders ef hægt er
def sameignafolders(filepath):
    count = 0
    count2 = 0
    done = False
    directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == 1]
    count2 = directories.count(directories[-1])
    licycle = cycle(directories)
    needUpdate = False
    y = next(licycle)
    while(done == False):
        if needUpdate == True:
            directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == 1]
            count2 = directories.count(directories[-1])
            licycle = cycle(directories)
            needUpdate = False
        x, y = y, next(licycle)
        if x == directories[-1]:
            count += 1
            if count == count2:
                done = True
        Rex = x.replace('downloads\\','')
        Rey = y.replace('downloads\\','')
        newPathyTox = filepath/Rex
        try:  
            samaheiti = re.match(Rex,Rey)
            if samaheiti != None:
                moveFiles(y,newPathyTox)
                print("Moved ", y)
                needUpdate = True
        except:
            pass



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

    #Röðin til að keyra kóðann sem ég var að gera :::
    #driverFolders(filepath)
    #driverFilesOnly(filepath) 
    #sameignafolders(filepath)  

    for x, y, z in os.walk(filepath):
       
        #works with directory to check if the name
       # ble = Path(x)
       # print(ble)
        #print(work_with_dir(x, filepath))
        work_with_file(z, x, filepath)
    return some
        

#Búa til fall til þess að lesa, nota regex til að gera það

print(search('downloads'))