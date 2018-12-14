import urllib
from urllib.request import urlopen
import json
import re
from pathlib import Path
import os
import shutil

def gettype(title):
    some_title = title.replace(' ', '%20')
    print(some_title)
    url = 'http://www.omdbapi.com/?apikey=852159f0&t='+some_title
    
    ble = urlopen(url)
    json_data = json.loads(ble.read())

  #  print(json_data["Type"])
    print(json_data)
gettype("How I met your mother - the best man")

season1 = re.compile('(S|s)[0-9][0-9]?')
season2 = re.compile('(S|s)eason [0-9]?[0-9]')
season3 = re.compile(' ?[0-9]?[0-9]x[0-9][0-9]')
season4 = re.compile(' ?[0-9][0-9][0-9][0-9]? ')

def work_with_shows(folder, files):
    #print(files)
    for i in files:
        current_path = os.path.join(folder, i)
        print(current_path)
        filename = i.replace('.', ' ')
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
                #print(os.path.join(folder, season_output))
            else:
                season_output = season + match4[0]
            
        else:
            season_output = 'Unknown'
        path_to_show = os.path.join(folder, season_output, i)
        new_path = os.path.dirname(path_to_show)
        print(path_to_show)    
        if os.path.isdir(new_path):
            try:
                shutil.move(current_path, path_to_show)
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
        if re.match(r'$Season [0-9]$', path_x.name): #skip already sorted shows
            continue
        elif path_x.parent == shows: #ignore the very first folder
            work_with_shows(x, z)
            print("sorted " + x)
            continue
        else:
            clean_out_of_subdirs(x, z, path_x.parent)
        #Go through all the subdirectories if their name isn't season something and put it in the main folder
            

def clean_out_of_subdirs(dirname, files, show_folder):
    for f in files:
        old_path = os.path.join(dirname, f)
        new_path = os.path.join(show_folder, f)
        shutil.move(old_path, new_path)

#sort_shows('downloads/Series')
movie_year = re.compile(' [0-9]{4} ')
movie_episode = re.compile(' Episode V?I{0,3}V?')



#til að sorteira myndirnar
def movie_orginizer(folder, movie):
    for i in movie:
        ble = i.replace('.', ' ')
        gtmovie = re.search(movie_year, ble)
        get_episode = re.search(movie_episode, ble)
        if gtmovie:
            movie1 = gtmovie.group()

def sort_movies(movie_folder):
    movies = Path(movie_folder)
    for x, y, z in os.walk(movies):
        if re.match('Season [0-9][0-9]?$', x):
            continue
        movie_orginizer(x, z)
