import requests  # download html
from bs4 import BeautifulSoup  # get data from html
from tabulate import tabulate

def rotten_tomatoes(search_list):
    '''
    scrape Rotten Tomatoes and return dict {search term: title, year, score}
    '''
    dict_rt = {}
    for search in search_list:
        try:
            res = requests.get('https://www.rottentomatoes.com/search?search=' + str(search).replace(' ','%20'))
            soup = BeautifulSoup(res.text, 'html.parser')
            title = (soup.find('search-page-media-row').get_text().strip())
            year = (soup.find('search-page-media-row')['releaseyear'])
            tomato_score = (soup.find('search-page-media-row')['tomatometerscore'])            
        except AttributeError:
            pass
        else:
            dict_rt[search] = [title, year, tomato_score]
    return(dict_rt)

def metacritic(search_list):
    '''
    scrape metacritic and return dict {search term: title, year, score}
    '''
    dict_mc = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'}
    for search in search_list:
        try:
            res = requests.get('https://www.metacritic.com/search/movie/' + str(search).replace(' ','%20') + '/results',headers = headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = (soup.find('div', 'main_stats').find('h3').get_text().strip())
            year = (soup.find('div', 'main_stats').find('p').get_text().strip().split(", ")[1])
            mc_score = (soup.find('div', 'main_stats').find('span').get_text())
        except AttributeError:
            pass            
        else:
            dict_mc[search] = [title, year, mc_score]
    return(dict_mc)

def combine(search_list,*results):
    '''
    merge results into dict of dicts
    index 0 = rotten tomatoes
    index 1 = metacritic
    '''
    merge = {k:[] for k in search_list}
    for search in search_list:
        for i,d in enumerate(results):
            if search in d.keys():
                item = {i:d[search]}
                merge[search].append(item)
    return merge

def app():
    search_list = ['dune','tick tick boom','shrek']    
    rt = rotten_tomatoes(search_list)
    mc = metacritic(search_list)    
    table = combine(search_list, rt,mc)
    print(tabulate(table))

if __name__ == '__main__':
    app()

'''
NOTES:
scenario 1: all sites have ratings
scenario 2: all sites have ratings but title/year does not match
scenario 3: only 1 site has rating
scenario 4: all sites no rating


& operator for intersection of dict
^ operator for symmetric difference for dict
| operator merge dict
'''
