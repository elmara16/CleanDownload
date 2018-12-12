import urllib
from urllib.request import urlopen
import json
import re
from pathlib import Path
import os
def gettype(title):
    someitle = title.replace(' ', '%20')
    url = 'http://www.omdbapi.com/?apikey=852159f0&t='+someitle
    ble = urlopen(url)
    json_data = json.loads(ble.read())
    print(json_data["Type"])
    print(json_data)
gettype("Star wars")

season1 = re.compile('(S|s)[0-9][0-9]?')
season2 = re.compile('(S|s)eason [0-9]?[0-9]')
season3 = re.compile(' [0-9]?[0-9]x[0-9][0-9]')
season4 = re.compile(' [0-9]?[0-9][0-9][0-9] ')

def work_with_shows(folder, files):
    counter = 0
    for i in files:
        filename = i.replace('.', ' ').replace('[', ' ')
        patt1 = re.search(season1, filename)
        patt2 = re.search(season2, filename)
        patt3 = re.search(season3, filename)
        patt4 = re.search(season4, filename)
        if patt1:
            match1 = patt1.group()
            season = match1.replace(match1, 'Season ')
            season_output = season + str(int(match1[1:3]))
        elif patt2:
            match2 = patt2.group()
            season_output = match2
        elif patt3:
            match3 = patt3.group()
            season = match3.replace(match3, 'Season ')
            season_output = season + str(int(match3.split('x')[0]))
        elif patt4:
            match4 = patt4.group().strip()
            season = match4.replace(match4, 'Season ')
            if len(season) == 4:
                season_output = season + str(int(match4[0:2]))
            else:
                season_output = season + match4[0]
        else:
            season_output = 'Unknown'
        path_to_show = os.path.join(folder, season_output)
       # print(path_to_show) 
        #Hér færa á milli
        try:
            os.mkdir(path_to_show)
            print('created directory' + season_output)
        except FileExistsError:
            print("Directory already exists")

def sort_shows(show_folder):
    shows = Path(show_folder)
    for x, y, z in os.walk(shows):
        work_with_shows(x, z)

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
        movie_orginizer(x, z)
