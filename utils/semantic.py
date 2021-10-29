import requests
import json

SEMANTIC_BASE_URL = 'https://api.semanticscholar.org/'
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
    def __init__(self, doi):
        resp = requests.get(SEMANTIC_PAPER_SEARCH_URL+doi).content
        article = json.loads(resp)
        self.citations = [gen(paper) for paper in article['citations']]
        self.references = [gen(paper) for paper in article['references']]
        self.authors = [author['name'] for author in article['authors']]
        self.url = doi
        self.fields = article['fieldsOfStudy']
        self.venue = article['venue']
        self.title = article['title']
        self.abstract = article['abstract']
        self.year = article['year']

def search(key):
    resp = requests.get(SEMANTIC_PAPER_KEYSEARCH_URL, params={'query':key, 'offset':0, 'limit':10, 'fields':'title,authors,year,externalIds,abstract,venue,citationCount,fieldsOfStudy'}).content
    papers = json.loads(resp)['data']
    #for paper in papers:


if __name__ == '__main__':
    # Article('10.1016/j.neucom.2021.01.130')
    search('graph')