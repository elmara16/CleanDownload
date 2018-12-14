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

season1 = re.compile('(S|s)[0-9][0-9]?')
season2 = re.compile('(S|s)eason [0-9]?[0-9]')
season3 = re.compile(' ?[0-9]?[0-9]x[0-9][0-9]')
season4 = re.compile(' ?[0-9]?[0-9] ?[0-9][0-9] ')

#Tears up folders and files so we can test the on database
def regexclean(line):
    line = line.split('\\')[-1].title().strip() # remove everything befor last \\ and last \\
    line = re.sub(r'\[[^()]*\]', '', line)  # remove everything inside []
    line = re.sub(r'\([^()]*\)', '', line) # remove everything inside ()
    line = re.sub(r'\{[^()]*\}', '', line) # remove everything inside {}
    line1 = re.search('([^\\\]+)\.(avi|mkv|mpeg|mpg|mov|mp4|)$', line) # find if it ends with .avi,.mp4 ...
    if line1:
        line = line1.group(1) # takes lines back together with evertyhing that is not in line1 i
    line = line.replace('.', ' ').lower()
    line2 = re.search('(.*?)(srt|mp4|mp3|avi$|dvdrip|hd|xvid|hdtv|dvdscr|brrip|divx|[\{\(\[]?[0-9]{4}).*', line) # takes everything with str,mp4... and what is behind the words selected
    if line2:
        line = line2.group(1) # takes lines back together with evertyhing that is not in line2
    line3 = re.search('(.*?)(blueray|240p|360p|480p|720p|1080p|[\{\(\[]?[0-9]{4}).*', line)    # remove resolation
    if line3:
        line = line3.group(1)
    line = line.strip() #remove all the leading and trailing spaces
    line3 = re.search('(.*?)([0-9]x[0-9]{2}|[a-z],|[0-9] +sería|seria [0-9]|[0-9]{3}|s[0-9]|e[0-9]|[0-9],|[0-9]{2}x[0-9]{2}|[0-9]-[0-9]|s[0-9]{2}|seasons|season|s[0-9]{2}[e][0-9]{2}|[\{\(\[]?[0-9]{4}).*', line)  # remove season etc.
    if line3:
        line = line3.group(1)
    line = line.strip()
    line4 = re.search('(.*?)(бsl texti|unrated rerip$|ch4|╓sl texti|uk$|m4v$| us$| uncut$| ca$|extended|isltexti|cut$|fxg$|us$| ice$|the complete$|torrent$|ísl|®|[\{\(\[]?[0-9]{4}).*', line) # remove more trash
    if line4:
        line = line4.group(1)
    line = line.strip()
    line5 = re.search('(.*?)(robin williams kuth$|axxo$|direcors cut$|el rey de la habana$|[\{\(\[]?[0-9]{4}).*', line) #remove more trash with seeders names or actors etc.
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
    line = re.sub(r'\([^()]*\)', '', line)
    line = re.sub(' +',' ',line)
    line = line.strip() #remove all the leading and trailing spaces
    return line
    
def gettype(title):
    title = title.replace(' ', '%20') # add %20 instead of space becasuse website works that way.
    try:
        url = 'http://www.omdbapi.com/?apikey=852159f0&t='+title # check if title of movie/series exists in database
        ble = urlopen(url)
        json_data = json.loads(ble.read())
        return(json_data['Type'])  # ask what type it is.
    except:
        return("None")

# Moves folders and files
def moveFiles(pathTocurrentFile, pathToNewDestination):
    shutil.move(pathTocurrentFile, pathToNewDestination)

#Working with only paths, num is for if we do need one \\ when it is in download or two \\ in series or movie
def driverFolders(filepath, num):
    count = 0 #default settings
    count2 = 0 #default settings
    done = False
    for x in listdir(filepath):
        newdir = Path(x).name.title().strip()
        match = re.match("Season [0-9]?[0-9]", newdir)
        if match:
            matc = match.group()
            path = Path(filepath)/matc
            files = listdir(path)
            clean_out_of_subdirs(path, files, filepath)
    directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == num] ## diectories that apear when filpeath is opened
    count2 = directories.count(directories[-1]) # how many times last word appears in directories
    licycle = cycle(directories) # cycle endless throw driectiories
    while(done == False): # runs until the last name of directories has appeard as many times as it is in directories
        x = next(licycle) # next index
        if x == directories[-1]: 
            count += 1
            if count == count2:
                done = True
        Rex = regexclean(x).title()  # cleans up path 
        dirName = filepath/Rex #path
        createAndMoveFile(x,dirName)

def createAndMoveFile(x, dirName):
    if not os.path.exists(dirName): # if path does not exists create new one. 
            Path.mkdir(dirName) #If x was how.met.your.mother. this will create folder how i met your mother
    else:    
        pass
    try:
        moveFiles(x, dirName)  # moves folder to new path 
    except:
        pass

#Working on files after folders have been workt on     
def driverFilesOnly(filepath,typer):
    onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))] # only files in filepath
    count = 0
    count2 = 0
    done = False 
    count2 = onlyfiles.count(onlyfiles[-1]) 
    licycle = cycle(onlyfiles)
    while(done == False):
        x = next(licycle)
        if x == onlyfiles[-1]:
            count += 1
            if count == count2:
                done = True
        Rex = regexclean(x).title()
        dirName = filepath/Rex
        dirFile = "downloads\\" + typer + x # typer is to know where is should go, just downloads folder or series, movie
        createAndMoveFile(dirFile,dirName)  # if folder dirname dose not exists create new one. If there is none this will create folder for file
   
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
        if 'season' not in Rex and 'Season' not in Rex: # So database dosent say season folder is movie or series 
            seriesOrMovies = gettype(Rex).title()
        else:
            seriesOrMovies = 'None'
        if Rex.title() != 'Series' and Rex.title() != 'Movie' and Rex.title() !='None': # So we dont and Series folder to Movie folder and None to Series etc..
            if not os.path.exists(filepath/seriesOrMovies): # if type of folder dosen't exists create one
                Path.mkdir(filepath/seriesOrMovies)
            else:    
                pass
            try:
                if seriesOrMovies == 'Series': # if type from data is Series move folder to series folder
                    moveFiles(x, filepath/seriesOrMovies) 
                elif seriesOrMovies == 'Movie':
                    moveFiles(x, filepath/seriesOrMovies)
                elif seriesOrMovies == 'None':
                    moveFiles(x, filepath/seriesOrMovies)
                else:
                    pass
            except:
                pass


def work_with_shows(folder, files):
    #print(files)
    for i in files:
        current_path = folder/i
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
            #print(hello)
        elif patt4:
            match4 = patt4.group().strip()
            season = match4.replace(match4, 'Season ')
            #print('im here')
            if len(match4) == 4:
                season_output = season + str(int(match4[0:2]))
            else:
                season_output = season + match4[0]
            
        else:
            season_output = 'Unknown'
        #Create a new path to the show
        path_to_show = folder/season_output/i
        new_path = os.path.dirname(path_to_show)
       # if there isn't a directory called season X create it before moving the files to it    
        if os.path.isdir(new_path):
            try:
                moveFiles(current_path, path_to_show)
            except:
                pass
        else:
            try:
                os.mkdir(new_path)
                shutil.move(current_path, path_to_show)
            except:
                pass            

def sort_shows(show_folder):
    shows = Path(show_folder)
    for x, y, z in os.walk(shows, topdown=False):
        path_x = Path(x)
        #ignore if the filename is season something
        if re.fullmatch(r'^Season [1-9]?[0-9]$', path_x.name): #skip already sorted shows
            continue
        elif path_x.parent != shows: #ignore the very first folder
            clean_out_of_subdirs(path_x, z, path_x.parent)#
            continue
            
        else:
            #Go through all the subdirectories if their name isn't season something and put it in the main folder
            work_with_shows(path_x, z)
    #for x, y, z in os.walk(shows):
    #    work_with_shows(Path(x), z)
    empty_files = listdir(show_folder)        
    for i in empty_files:
        try:
            shutil.rmtree(i)
        except:
            pass     

#moves files from sub folder to the main folder
def clean_out_of_subdirs(dirname, files, show_folder):
    for f in files:
        old_path = dirname/f
        new_path = Path(show_folder)/f
        moveFiles(old_path, new_path)


def moveFoldersToSeriesorMovies(filepath):
    dirname = filepath/'None'
    goToS = filepath/'Series'
    goToM = filepath/'Movie'
    directories2 = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 3] # get all folder inside download filepath
    for x in listdir(filepath):
        newdir = Path(x).name.title().strip()
        match = re.match("Season [0-9]?[0-9]", newdir)
        if match:
            matc = match.group()
            path = Path(filepath)/matc
            files = listdir(path)
            clean_out_of_subdirs(path, files, filepath)
    for folder in directories2:
        newdir = folder.title().strip()
        newdir = re.sub('1080p','', newdir) # take out 1080p it confuses sendToMovie search
        sendToSeries = re.search('[0-9][0-9]-[0-9]|season|episodes|s[0-9]|s[0-9]{2}e[0-9]{2}|series', newdir) # if in folder is one of this move it to series
        if sendToSeries != None:
            try:
                moveFiles(folder, goToS)
            except:
                pass
        sendToMovie = re.search('[0-9]{4}',newdir) # if year is in file move to movies
        if sendToMovie != None:
            try:
                moveFiles(folder,goToM)
            except:
                pass
    directories = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 2] # Update to see what files are empty
    remove_empyfiles(directories)
            
def moveFilesToSeriesorMovies(filepath):
    dirname = filepath/'None'
    goToS = filepath/'Series'
    goToM = filepath/'Movie'
    directories = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 2]
  
    for folder in directories:
        folder2 = os.listdir(folder)
        for file2 in folder2:
            OldDirname = folder +'\\'+ file2 
            file2 = re.sub('1080p','', file2).lower()
            fix = file2.replace('.', ' ') 
            fix = fix.replace('-', ' ' )
            fix = fix.replace('_', ' ') # taking out confusing characters
            fix = [int(s) for s in fix.split() if s.isdigit()]
            fix = [g for g in fix if len(str(g)) > 4 and g > 1500] # ignore numbers size > 4 and number less than 1500, movies are more likly to be made later than 1500
            sendToSeries = re.search('e[0-9]{2}|[0-9]-[0-9]|season|episodes|s[0-9]|s[0-9]{2}e[0-9]{2}|Series', file2)
            if sendToSeries != None:
                try:
                    moveFiles(OldDirname, goToS)
                except:
                    pass
            if len(fix) == 0: # if size is null, than it must be year
                sendToMovie = re.search('[0-9]{4}',file2)
                if sendToMovie != None:
                    try:
                        moveFiles(OldDirname,goToM)
                    except:
                        pass
    remove_empyfiles(directories)  

#Removes folder if it is empty
def remove_empyfiles(directories):
    for folder in directories:
        if not os.listdir(folder):
            os.rmdir(folder)   

#Move files and folder to None if it hasen't been moved yet from folder
def restOfFilesToNone(filepath):
    a = os.listdir(filepath) # in dowload folder
    newDirName = filepath/'None' # new path
    for x in a:
        oldDirName = 'downloads//' + x
        if x != 'Movie' and x != 'Series' and x != 'None': # if file or folder does not have thease names move them to None
            try:
                moveFiles(oldDirName, newDirName)
            except:
                pass

def main(foldername):
    filepath = Path(foldername)
    driverFolders(filepath,1)
    driverFilesOnly(filepath, '')
    moveFoldersToTypes(filepath) 
    moveFoldersToSeriesorMovies(filepath)
    moveFilesToSeriesorMovies(filepath)
    driverFolders(filepath/'Series',2)
    driverFilesOnly(filepath/'Series', 'Series\\')
    driverFolders(filepath/'Movie',2)
    driverFilesOnly(filepath/'Movie', 'Movie\\')
    #sort_shows('downloads/Series')
    restOfFilesToNone(filepath)

if __name__ == '__main__':
    main('downloads')