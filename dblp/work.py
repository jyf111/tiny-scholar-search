import requests
from lxml import etree

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'
DBLP_PERSON_URL = DBLP_BASE_URL + 'pid/{pid}.xml'

lazy_db = {}

def gen_author(pid):
    if pid in lazy_db:
        return lazy_db[pid]
    else:
        author = Author(pid)
        lazy_db[pid] = author
        return author

class Author():
    def __init__(self, pid):
        self.pid = pid
        xml = requests.get(DBLP_PERSON_URL.format(pid=pid)).content
        root = etree.fromstring(xml)
        self.name = root.attrib['name']
        self.papers = root.attrib['n']
        self.affiliations = root.xpath('/dblpperson/person/note/text()')
        self.publications = [{'author':[]} for _ in range(int(self.papers))]
        for i, r in enumerate(root.xpath('/dblpperson/r')):
            pub = self.publications[i]
            for son in r.iter():
                if son.tag=='author':
                    pub[son.tag].append('<a href=\'/author-pid=' + son.attrib['pid'] + '\'>' + son.text + '</a>') # TODO gen_author ?
                elif son.tag in ('title', 'year', 'ee'):
                    pub[son.tag] = son.text
                elif son.tag in ('journal', 'booktitle'):
                    pub['kind'] = son.text
            self.publications[i] = pub

def search(author_str):
    resp = requests.get(DBLP_AUTHOR_SEARCH_URL, params={'xauthor':author_str})
    root = etree.fromstring(resp.content)
    authors = []
    for author in root.xpath('/authors/author'):
        authors.append({'pid': author.attrib['pid'], 'name': author.text})
    return authors

if __name__ == '__main__':
    search('xuelong li')