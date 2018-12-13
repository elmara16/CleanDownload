#!/usr/bin/env python
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


#Tætar í sig files og folders
def regexclean(line):
    line = line.split('\\')[-1].title().strip()
    line = re.sub(r'\[[^()]*\]', '', line)
    line = re.sub(r'\([^()]*\)', '', line)
    line = re.sub(r'\{[^()]*\}', '', line)
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
    line3 = re.search('(.*?)([0-9]x[0-9]{2}|[a-z],|[0-9] +sería|seria [0-9]|[0-9]{3}|s[0-9]|e[0-9]|[0-9],|[0-9]{2}x[0-9]{2}|[0-9]-[0-9]|s[0-9]{2}|seasons|season|s[0-9]{2}[e][0-9]{2}|[\{\(\[]?[0-9]{4}).*', line)
    if line3:
        line = line3.group(1)
    # annad rusl
    line = line.strip()
    line4 = re.search('(.*?)(бsl texti|unrated rerip$|ch4|╓sl texti|uk$|m4v$| us$| uncut$| ca$|extended|isltexti|cut$|fxg$|us$| ice$|the complete$|torrent$|ísl|®|[\{\(\[]?[0-9]{4}).*', line)
    if line4:
        line = line4.group(1)
    line = line.strip()
    # meira rusl t.d. nofn a deilendum, leikurum
    line5 = re.search('(.*?)(robin williams kuth$|axxo$|direcors cut$|el rey de la habana$|[\{\(\[]?[0-9]{4}).*', line)
    if line5:
        line = line5.group(1)
    if ';' in line:
        line = line.split(';')
        line = line[1]
        line = "".join(line)
    line = re.sub(r'^s[0-9]{2}e[0-9]{2}', '',line)
    line = line.replace('-', ' ')
    line = re.sub("' ", '',line)
    line = line.replace("_", ' ')
    line = line.replace("", '')
    line = re.sub(r'\([^()]*\)', '', line)
    line = re.sub(' +',' ',line)
    line = line.strip()
    return line
    
def gettype(title):
    title = title.replace(' ', '%20')
    try:
        url = 'http://www.omdbapi.com/?apikey=852159f0&t='+title
        ble = urlopen(url)
        json_data = json.loads(ble.read())
        return(json_data['Type'])
    except:
        return("None")

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
        Rex = regexclean(x).title()
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
        Rex = regexclean(x).title()
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

def moveFoldersToTypes(filepath):
    count = 0
    count2 = 0
    done = False
    directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == 1]
    count2 = directories.count(directories[-1])
    licycle = cycle(directories)
    while(done == False):
        x = next(licycle)
        if x == directories[-1]:
            count += 1
            if count == count2:
                done = True
        Rex = x.replace('downloads\\','')
        if 'season' not in Rex and 'Season' not in Rex:
            seriesOrMovies = gettype(Rex).title()
        else:
            seriesOrMovies = 'None'
        if Rex.title() != 'Series' and Rex.title() != 'Movie' and Rex.title() !='None':
            if not os.path.exists(filepath/seriesOrMovies):
                Path.mkdir(filepath/seriesOrMovies)
                print("Directory " , seriesOrMovies ,  " Created ")
            else:    
                print("Directory " , seriesOrMovies ,  " already exists")
            try:
                if seriesOrMovies == 'Series':
                    moveFiles(x, filepath/seriesOrMovies)
                    print('Move', x)
                elif seriesOrMovies == 'Movie':
                    moveFiles(x, filepath/seriesOrMovies)
                    print('Move', x)
                elif seriesOrMovies == 'None':
                    moveFiles(x, filepath/seriesOrMovies)
                    print('Move', x)
                else:
                    pass
            except:
                pass

season1 = re.compile('(S|s)[0-9][0-9]?')
season2 = re.compile('(S|s)eason [0-9]?[0-9]')
season3 = re.compile(' [0-9]?[0-9]x[0-9][0-9]')
season4 = re.compile(' [0-9][0-9][0-9][0-9]? ')

def work_with_shows(folder, files):
    #print(files)
    for i in files:
        current_path = os.path.join(folder, i)
        filename = i.replace('.', ' ').replace('[', ' ')
        patt1 = re.search(season1, filename)
        patt2 = re.search(season2, filename)
        patt3 = re.search(season3, filename)
        patt4 = re.search(season4, filename)
        if patt1:
            match1 = patt1.group()
            season = match1.replace(match1, 'Season ')
            season_output = season + str(int(match1[1:]))
        elif patt2:
            match2 = patt2.group()
            season_output = match2
        elif patt3:
            match3 = patt3.group().strip()
            season = match3.replace(match3, 'Season ')
            season_output = season + str(int(match3.split('x')[0]))
        elif patt4:
            match4 = patt4.group().strip()
            season = match4.replace(match4, 'Season ')
            #print('im here')
            if len(match4) == 4:
                season_output = season + str(int(match4[0:2]))
                print(os.path.join(folder, season_output))
            else:
                season_output = season + match4[0]
            
        else:
            season_output = 'Unknown'
        path_to_show = os.path.join(folder, season_output, i)
        new_path = os.path.dirname(path_to_show)
        print(path_to_show)    
        if os.path.isdir(new_path):
            try:
                moveFiles(current_path, new_path)
            except:
                pass
        else:
            try:
                os.mkdir(new_path)
                shutil.move(current_path, new_path)
            except:
                pass            

def moveFoldersToSeriesorMovies(filepath):
    dirname = filepath/'None'
    goToS = filepath/'Series'
    goToM = filepath/'Movie'
    a = os.listdir(dirname)
    directories = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 2]
    directories2 = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 3]
    lis = [os.listdir(x) for x in directories]
    for x in directories:
        newdir = x.split('\\')[-1].title().strip()
        if "Season" in newdir:
            try:
                moveFiles(x, goToS)
            except:
                pass
    for z in directories2:
        newdir = z.split('\\')[-1].title().strip().lower()
        newdir = re.sub('1080p','', newdir)
        sendToSeries = re.search('[0-9]-[0-9]|season|episodes|s[0-9]|s[0-9]{2}e[0-9]{2}|Series', newdir)
        if sendToSeries != None:
            try:
                moveFiles(z, goToS)
            except:
                pass
        sendToMovie = re.search('[0-9]{4}',newdir)
        if sendToMovie != None:
            try:
                moveFiles(z,goToM)
            except:
                pass
    for z in directories:
        if not os.listdir(z):
            print('deleted folder', z)
            os.rmdir(z)
            


def search(foldername):
    filepath = Path(foldername)
    
    #driverFolders(filepath)
    #driverFilesOnly(filepath) 
    #moveFoldersToTypes(filepath) 

    #moveFoldersToSeriesorMovies(filepath)
    moveFilesToSeriesorMovies(filepath)


#Búa til fall til þess að lesa, nota regex til að gera það
if __name__ == '__main__':
    main('downloads')