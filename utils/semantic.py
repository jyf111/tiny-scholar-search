import requests
import json

SEMANTIC_BASE_URL = 'https://api.semanticscholar.org/'
SEMANTIC_PAPER_SEARCH_URL = SEMANTIC_BASE_URL + 'v1/paper/'

def search(doi):
    resp = requests.get(SEMANTIC_PAPER_SEARCH_URL+doi).content
    article = json.loads(resp)
    print(article['abstract'])

if __name__ == '__main__':
    search('10.1016/J.AMC.2021.126178')