import requests
from lxml import etree

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_AUTHOR_SEARCH_URL = DBLP_BASE_URL + 'search/author'
DBLP_PERSON_URL = DBLP_BASE_URL + 'pid/{pid}.xml'

headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

lazy_db = {}
rank_db = {}

def gen_author(pid):
    if pid in lazy_db:
        return lazy_db[pid]
    else:
        author = Author(pid)
        lazy_db[pid] = author
        return author

def get_rank(type):
    if len(rank_db)==0: # init rank_db
        with open('static/ccfrank.txt', 'r') as f:
            while True:
                cur = f.readline()
                if not cur:
                    break
                rank_db[cur[2:-1]] = cur[0].lower()
    type = '/' + type
    if type in rank_db:
        return rank_db[type]
    else:
        return "none"
        
class Author():
    def __init__(self, pid):
        self.pid = pid
        xml = requests.get(DBLP_PERSON_URL.format(pid=pid), headers=headers).content
        root = etree.fromstring(xml)
        self.name = root.attrib['name']
        self.papers = root.attrib['n']
        self.affiliations = root.xpath('/dblpperson/person/note/text()')
        self.publications = [{'author':[]} for _ in range(int(self.papers))]
        self.ccfa, self.ccfb, self.ccfc, self.ccfnone = 0, 0, 0, 0
        self.journals, self.conferences = 0, 0
        for i, r in enumerate(root.xpath('/dblpperson/r')):
            pub = self.publications[i]
            for son in r.iter():
                if son.tag=='author':
                    pub[son.tag].append(['<a href=\'/author=' + son.attrib['pid'] + '\'>' + son.text + '</a>', son.text])
                elif son.tag in ('year', 'ee'):
                    pub[son.tag] = son.text
                elif son.tag in ('journal', 'booktitle'):
                    pub['kind'] = son.text
                    pub['type'] = ('Journal' if son.tag=='journal' else 'Conference')
                    if pub['type']=='Journal':
                        self.journals += 1
                    else:
                        self.conferences += 1
                elif son.tag=='title':
                    result = ""
                    include = False
                    for c in etree.tostring(son):
                        c = chr(c)
                        if c=='<':
                            include = True
                        elif c=='>':
                            include = False
                        elif (not include) and c!='\n':
                            result += c
                    pub['title'] = result
                elif 'key' in son.attrib:
                    pub['key'] = son.attrib['key']
                    tmp = son.attrib['key'].split('/')
                    pub['rank'] = get_rank(tmp[0]+'/'+tmp[1])
                    if pub['rank']=='a':
                        self.ccfa += 1
                    if pub['rank']=='b':
                        self.ccfb += 1
                    if pub['rank']=='c':
                        self.ccfc += 1
                    if pub['rank']=='none':
                        self.ccfnone += 1
            self.publications[i] = pub

def like(a, b):
    i = len(a) - 1
    while i>=0 and a[i].isdigit():
        i -= 1
    return a[:i+1].lower().strip()==b.lower().strip()

def search(author_str):
    resp = requests.get(DBLP_AUTHOR_SEARCH_URL, headers=headers, params={'xauthor':author_str})
    root = etree.fromstring(resp.content)
    exact_authors, likely_authors = [], []
    for author in root.xpath('/authors/author'):
        if like(author.text, author_str):
            exact_authors.append({'pid': author.attrib['pid'], 'name': author.text})
        else:
            likely_authors.append({'pid': author.attrib['pid'], 'name': author.text})
    return exact_authors, likely_authors

if __name__ == '__main__':
    Author('l/XuelongLi')