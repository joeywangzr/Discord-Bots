# from bs4 import BeautifulSoup
# import requests
# import json

# def grabnews():
    
    
#     soup = BeautifulSoup
#     headlines = soup.find_all{attrs={"itemprop": "headline"}}

from bs4 import BeautifulSoup
import requests
import json

def headlinegrabber(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    headlines = soup.findAll(attrs={"class": "headline"})
    listHeadlines = []
    x = 0
    for headline in headlines:
        if 0 < x < 6:
            listHeadlines.append(headline.text)
            x = x + 1
        else:
            x = x + 1

    return listHeadlines

# def headlinegrabber(response_text):
#     soup = BeautifulSoup(response_text, 'lxml')
#     headlines = soup.find_all('a')
#     x=0
#     for headline in headlines:
#         if x < 32:
#             x = x+1  
#         elif 37 > x > 31:
#             x = x + 1
#             print(headline.text)
#             print('')



# url = 'https://www.cbc.ca/news'
# response = requests.get(url)
# headlinegrabber(response.text)



# import httplib2
# from bs4 import BeautifulSoup, SoupStrainer

# http = httplib2.Http()
# status, response = http.request('http://www.nytimes.com')

# for link in BeautifulSoup(response, 'lxml', parse_only=SoupStrainer('a')):
#     if link.has_attr('href'):
#         print(link['href'])