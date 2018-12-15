#!/usr/bin/env python
import os
from pathlib import Path
import re
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

#Tears up folders and files so we can test them on database
def regexclean(line):
    line = line.split('\\')[-1].title().strip() # remove everything before last \\ and also last \\
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
    count = 0 #default settings how many times the last folder has appear in currend stat in loop
    count2 = 0 #default settings how many times it appears
    done = False
    for x in listdir(filepath): #check all the subdirs
        newdir = Path(x).name.title().strip()
        match = re.match("Season [0-9]?[0-9]", newdir)
        if match: #if there is a season in the given folder
            matc = match.group()
            path = Path(filepath)/matc
            files = listdir(path)
            clean_out_of_subdirs(path, files, filepath) #clear everything out of the folder
    directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == num] ## diectories that apear when filpeath is opened
    count2 = directories.count(directories[-1]) # how many times last word appears in directories
    licycle = cycle(directories) # cycle endless throw driectiories
    while(done == False): # runs until the last name of directories has appeard as many times as it is in directories
        x = next(licycle) # next index (path)
        if x == directories[-1]: 
            count += 1
            if count == count2:
                done = True
        Rex = regexclean(x).title()  # cleans up path for database and to get folders with same names together. how.i.met.your.mother.s03e02 and how.i.met.yourmother. Will go to clean folder how i met your mother 
        NewDirName = filepath/Rex # new path
        createAndMoveFile(x,NewDirName) # x is the old folder path

def createAndMoveFile(oldPath, NewDirName):
    if not os.path.exists(NewDirName): # If path does not exists create new one. 
            Path.mkdir(NewDirName) # If oldPath was how.met.your.mother. this will create new folder how i met your mother
    else:    
        pass
    try:
        moveFiles(oldPath, NewDirName)  # moves folder or file to new path 
    except:
        pass

#Working on files after folders have been workt on, aloot of same logic as in driverfolderonly     
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
        NewPath = filepath/Rex
        oldPath = "downloads\\" + typer + x # typer is to know where it was, downloads, series or movie folder
        createAndMoveFile(oldPath,NewPath)
   
def moveFoldersToTypes(filepath):
    count = 0
    count2 = 0
    done = False
    directories = [x[0] for x in os.walk(filepath) if x[0].count('\\') == 1] ## diectories that appear when download file is opened
    count2 = directories.count(directories[-1])
    licycle = cycle(directories)
    while(done == False):
        x = next(licycle)
        if x == directories[-1]:
            count += 1
            if count == count2:
                done = True
        Rex = x.replace('downloads\\','') 
        if 'season' not in Rex and 'Season' not in Rex: # So database dosent say season folder is movie or series instead it goes to None
            seriesOrMovies = gettype(Rex).title()
        else:
            seriesOrMovies = 'None'
        if Rex.title() != 'Series' and Rex.title() != 'Movie' and Rex.title() !='None': # So we do not send Series folder to Movie folder and None to Series for example
            if not os.path.exists(filepath/seriesOrMovies): # if type of folder dosen't exists create one
                Path.mkdir(filepath/seriesOrMovies)
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
        #current path to the movie       
        current_path = folder/i
        #replace . with spaces to get rid of confusion in the filename
        filename = i.replace('.', ' ').replace('[', ' ')
        #Check if regex matches (see top of the file)
        patt1 = re.search(season1, filename)
        patt2 = re.search(season2, filename)
        patt3 = re.search(season3, filename)
        patt4 = re.search(season4, filename)
        if patt1: #if it's S01E01
            match1 = patt1.group()
            season = match1.replace(match1, 'Season ')
            season_output = season + str(int(match1[1:]))
        elif patt2: #if it's season xx
            match2 = patt2.group()
            season_output = match2
        elif patt3: #if it's 01x01 first is season and the other is episode
            match3 = patt3.group().strip()
            season = match3.replace(match3, 'Season ')
            season_output = season + str(int(match3.split('x')[0]))
            
        elif patt4: #if it's either 3 or 4 letters
            match4 = patt4.group().strip()
            season = match4.replace(match4, 'Season ')
            if len(match4) == 4:
                season_output = season + str(int(match4[0:2]))
            else:
                season_output = season + match4[0]
            
        else: #if it doesn't match any pattern its not known which season it is
            season_output = 'Unknown'
        #Create a new path to the show
        path_to_show = folder/season_output/i
        new_path = os.path.dirname(path_to_show)
       # if there isn't a directory called season X create it before moving the files to it    
        if Path(new_path).is_dir():
            try:
                moveFiles(current_path, path_to_show)
            except:
                pass
        else:
            try:
                os.mkdir(new_path)
                moveFiles(current_path, path_to_show)
            except:
                pass            

def sort_shows(shows):
    #shows = Path(show_folder)
    for i in listdir(shows):
        path = shows/i
        for x, y, z in os.walk(path):
            path_x = Path(x)
            #ignore if the filename is season something
            if re.fullmatch(r'^Season [1-9]?[0-9]$', path_x.name): #skip already sorted shows
                continue
            elif path_x.parent == shows: #ignore the very first folder
                continue
            else:
                clean_out_of_subdirs(path_x, z, path) #removes everything from subdirs
    
        #Get eveeything from the directory
        files = listdir(path)
        #sort the shows
        work_with_shows(path, files)
        

#moves files from sub folder to the main folder
def clean_out_of_subdirs(dirname, files, show_folder):
    for f in files:
        old_path = dirname/f
        new_path = show_folder/f
        moveFiles(old_path, new_path)

# Move folders that database could not move to series or movie
def moveFoldersFromNoneToSeriesorMovies(filepath):
    dirname = filepath/'None' # oldPath
    goToS = filepath/'Series' # move to series
    goToM = filepath/'Movie' # move to movie
    directories2 = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 3] # get all folders that appear when you open folders inside none folder. (None folder are ther parent parent)
    for x in listdir(filepath):
        newdir = Path(x).name.title().strip()
        match = re.match("Season [0-9]?[0-9]", newdir) #check if season X is name of folder
        if match: 
            matc = match.group()
            path = Path(filepath)/matc
            files = listdir(path)
            clean_out_of_subdirs(path, files, filepath) #clean everything out of the folder
    for folder in directories2:
        newdir = folder.title().strip()
        newdir = re.sub('1080p','', newdir) # take out 1080p it confuses sendToMovie search
        sendToSeries = re.search('[0-9][0-9]-[0-9]|season|episodes|s[0-9]|s[0-9]{2}e[0-9]{2}|series', newdir) # if in folder has one of this move it to series
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
    remove_empyfiles(directories) # remove empy files

# Move files that database could not move to series or movie     
def moveFilesFromNoneToSeriesorMovies(filepath):
    dirname = filepath/'None'
    goToS = filepath/'Series'
    goToM = filepath/'Movie'
    directories = [x[0] for x in os.walk(dirname) if x[0].count('\\') == 2] # get child folders of none folder
  
    for folder in directories:
        folder2 = os.listdir(folder) # get all files that are children of folders in directories
        for file2 in folder2:
            oldDirname = folder +'\\'+ file2 # old path
            file2 = re.sub('1080p','', file2).lower()
            fix = file2.replace('.', ' ') 
            fix = fix.replace('-', ' ' )
            fix = fix.replace('_', ' ') # taking out confusing characters
            fix = [int(s) for s in fix.split() if s.isdigit()]
            fix = [g for g in fix if len(str(g)) > 4 and g > 1500] # ignore numbers size > 4 and number less than 1500, movies are more likly to be made later than 1500
            sendToSeries = re.search('e[0-9]{2}|[0-9]-[0-9]|season|episodes|s[0-9]|s[0-9]{2}e[0-9]{2}|Series', file2) # if file has any of thease move to series
            if sendToSeries != None: 
                try:
                    moveFiles(oldDirname, goToS)
                except:
                    pass
            if len(fix) == 0: # if size is null, than it must be year
                sendToMovie = re.search('[0-9]{4}',file2)
                if sendToMovie != None:
                    try:
                        moveFiles(oldDirname,goToM)
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
    moveFoldersFromNoneToSeriesorMovies(filepath)
    moveFilesFromNoneToSeriesorMovies(filepath)
    driverFolders(filepath/'Series',2)
    driverFilesOnly(filepath/'Series', 'Series\\')
    driverFolders(filepath/'Movie',2)
    driverFilesOnly(filepath/'Movie', 'Movie\\')
    sort_shows(filepath/'Series')
    restOfFilesToNone(filepath)

if __name__ == '__main__':
    main('downloads')