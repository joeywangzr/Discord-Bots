from bs4 import BeautifulSoup
import requests

def webScrapeWeather(city):
    # enter city name
    
    # create url
    url = f"https://www.google.com/search?q=weather+{city}"
    
    # requests instance
    html = requests.get(url).content
    
    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    status = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text.split().pop()

    def hasNum(inputString):
        return any(char.isdigit() for char in inputString)

    for i in temp.split():
        if hasNum(i) == True:
            return(i, status)

# print(webScrapeWeather('calgary'))
