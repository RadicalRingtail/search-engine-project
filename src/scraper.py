import requests, wikipedia
from bs4 import BeautifulSoup
from functools import lru_cache

########################
# enviroment variables #
########################

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}

number_of_results = 10

use_google = True
use_bing = True
use_yahoo = True

##########################
# search engine scrapers #
##########################

@lru_cache(maxsize = None)
def scrape_google(url):
    html = requests.get(url=url, headers=header).text
    bs = BeautifulSoup(html, 'html.parser')
    
    title = []
    link = []
    desc = []
    engine = []

    for titles in bs.find_all('h3', {'class':'LC20lb'}):
        title.append(titles.text)
        engine.append('Google')

    for links in bs.find_all('div', {'class':'r'}):
        try:
            link.append(links.a['href'])
        except:
            pass

    for descs in bs.find_all('span', {'class':'st'}):
        desc.append(descs.text)

    return title, link, desc, engine

@lru_cache(maxsize = None)
def scrape_bing(url):
    html = requests.get(url=url, headers=header).text
    bs = BeautifulSoup(html, 'html.parser')

    title = []
    link = []
    desc = []
    engine = []

    for titles in bs.find_all('h2'):
        try:
            links = titles.a['href']
            engine.append('Bing')

            if ('http') not in links:
                pass
            else:
                title.append(titles.text)
                link.append(links)
        except:
            pass

    for descs in bs.find_all('div',{'class':'b_caption'}):
        try:
            desc.append(descs.p.text)
        except:
            desc.append('Description unavailable.')
    
    return title, link, desc, engine

def scrape_yahoo(url):
    pass

##################
# other scrapers #
##################

@lru_cache(maxsize = None)
def wikipedia_sraper(artical):
    try:
        page = wikipedia.page(title=artical, auto_suggest=True)
        info = wikipedia.summary(page, sentences=2)

        return(page.title, info)
    except:
        pass

###################
# extra functions #
###################

@lru_cache(maxsize = None)
def search(term):

    #url_yaho = 'https://search.yahoo.com/search?p={}'.format(term)

    results = []

    if use_google is True:
        google_results = scrape_google('https://www.google.com/search?q={}&num={}'.format(term.replace(' ', '+'), number_of_results))
        results.append(zip(google_results[0], google_results[1], google_results[2], google_results[3]))
    
    if use_bing is True:
        bing_results = scrape_bing('https://www.bing.com/search?q={}&count={}'.format(term.replace(' ', '+'), number_of_results))
        results.append(zip(bing_results[0], bing_results[1], bing_results[2], bing_results[3]))

    final_results = []

    for all_items in results:
        for item in all_items:
            if item[1] not in final_results:                
                final_results.append(item)

    print()
    return(final_results)