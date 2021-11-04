import requests
import json

SEMANTIC_BASE_URL = 'http://api.semanticscholar.org/'
SEMANTIC_PAPER_SEARCH_URL = SEMANTIC_BASE_URL + 'v1/paper/'
SEMANTIC_PAPER_KEYSEARCH_URL = SEMANTIC_BASE_URL + 'graph/v1/paper/search'

def gen(paper):
    result = {}
    result['authors'] = [author['name'] for author in paper['authors']]
    result['title'] = paper['title']
    result['venue'] = paper['venue']
    result['year'] = paper['year']
    result['doi'] = paper['doi']
    return result

class Article():
    def __init__(self, article, doi):
        if 'error' in article:
            self.error = article['error']
            return
        else:
            self.error = None
        if 'citations' in article:
            self.citations = [gen(paper) for paper in article['citations']]
        else:
            self.citations = []
        if 'citationCount' in article:
            self.citationCount = int(article['citationCount'])
        else:
            self.citationCount = len(article['citations'])
        if 'references' in article:
            self.references = [gen(paper) for paper in article['references']]
        else:
            self.references = []
        self.authors = [author['name'] for author in article['authors']]
        self.url = doi
        self.fields = article['fieldsOfStudy']
        self.venue = article['venue']
        self.title = article['title']
        self.abstract = article['abstract']
        self.year = article['year']

def genArticle(doi):
    resp = requests.get(SEMANTIC_PAPER_SEARCH_URL+doi).content
    article = json.loads(resp)
    return Article(article, doi)

def search(key):
    resp = requests.get(SEMANTIC_PAPER_KEYSEARCH_URL, params={'query':key, 'offset':0, 'limit':10, 'fields':'title,authors,year,externalIds,abstract,venue,citationCount,fieldsOfStudy'}).content
    result = json.loads(resp)
    if 'data' in result:
        papers = json.loads(resp)['data']
    else:
        papers = []
    articles = []
    for paper in papers:
        articles.append(Article(paper, ""))
    return articles

if __name__ == '__main__':
    # Article('10.1016/j.neucom.2021.01.130')
    search('graph')