import requests
import json

SEMANTIC_BASE_URL = 'http://api.semanticscholar.org/'
SEMANTIC_PAPER_SEARCH_URL = SEMANTIC_BASE_URL + 'v1/paper/'
SEMANTIC_PAPER_KEYSEARCH_URL = SEMANTIC_BASE_URL + 'graph/v1/paper/search'

headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

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
        if 'externalIds' in article:
            tmp = article['externalIds']
            if 'DOI' in tmp:
                self.url = tmp['DOI']
        self.fields = article['fieldsOfStudy']
        self.venue = article['venue']
        self.title = article['title']
        self.abstract = article['abstract']
        self.year = article['year']

def genArticle(doi):
    resp = requests.get(SEMANTIC_PAPER_SEARCH_URL+doi, headers=headers).content
    article = json.loads(resp)
    return Article(article, doi)

def search(key, start):
    resp = requests.get(SEMANTIC_PAPER_KEYSEARCH_URL, headers=headers, params={'query':key, 'offset':0, 'limit':10, 'offset':start, 'fields':'title,authors,year,externalIds,abstract,venue,citationCount,fieldsOfStudy'}).content
    result = json.loads(resp)
    if 'data' in result:
        papers = result['data']
    else:
        papers = []
    if 'total' in result:
        total = int(result['total'])
    else:
        total = 0
    articles = []
    for paper in papers:
        articles.append(Article(paper, "/"))
    return (total, articles)

if __name__ == '__main__':
    # Article('10.1016/j.neucom.2021.01.130')
    search('graph')
