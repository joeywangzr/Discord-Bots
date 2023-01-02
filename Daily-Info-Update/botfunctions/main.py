import requests
import json
from newsgrabber import headlinegrabber
from alarm import initTimer
from alarm import checkTime


url = 'https://www.cbc.ca/news'
response = requests.get(url)
headlinegrabber(response.text)




