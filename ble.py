import urllib
from urllib.request import urlopen
import json
def gettype(title):
    url = 'http://www.omdbapi.com/?apikey=852159f0&t='+title
    ble = urlopen(url)
    json_data = json.loads(ble.read())
    print(json_data)
gettype("24")


