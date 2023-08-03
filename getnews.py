import requests
from bs4 import BeautifulSoup


def getNewsVNEXPRESS():
    response = requests.get('https://vnexpress.net')
    soup = BeautifulSoup(response.text, 'html.parser')
    myDiv = soup.find_all("h3", {"class": "title-news"})

    listNews = []
    for new in myDiv:
        newsdict = {}
        newsdict["tittle"] = new.text
        newsdict["link"] = new.a.get("href")
        listNews.append(newsdict)

    return listNews

def getNewsDANTRI():
    response = requests.get('https://dantri.com.vn')
    soup = BeautifulSoup(response.text, 'html.parser')
    myDiv = soup.find_all("h3", {"class": "article-title"})

    listNews = []
    for new in myDiv:
        newsdict = {}
        newsdict["tittle"] = new.text
        newsdict["link"] = new.a.get("href")
        listNews.append(newsdict)

    return listNews