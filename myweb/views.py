from django.http import HttpResponse
from django.shortcuts import render, redirect
from pyecharts import options as opts
from pyecharts.charts import Bar
from random import randint
import utils.dblp
import utils.semantic
import time


def page(request):
    return render(request, 'index.html')

def scholarsearch(request):
    USERS_PER_PAGE = 4
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        message = request.GET['name']
    else:
        message = ''
    if 'start1' in request.GET and request.GET['start1']:
        start1 = int(request.GET['start1'])
    else:
        start1 = 0
    if 'start2' in request.GET and request.GET['start2']:
        start2 = int(request.GET['start2'])
    else:
        start2 = 0
    exact_authors, likely_authors = utils.dblp.search(message)
    exact_len, likely_len = len(exact_authors), len(likely_authors)
    if exact_len:
        start1 %= exact_len
    if likely_len:
        start2 %= likely_len
    exact_authors = exact_authors[start1:]
    likely_authors = likely_authors[start2:]
    if len(exact_authors)>USERS_PER_PAGE:
        exact_authors = exact_authors[:USERS_PER_PAGE]
    if len(likely_authors)>USERS_PER_PAGE:
        likely_authors = likely_authors[:USERS_PER_PAGE]
    return render(request, 'search/author.html', {'key': message, 'exact_authors': exact_authors, 'exact_len': exact_len, 'likely_authors': likely_authors, 'likely_len': likely_len})

def papersearch(request):
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        message = request.GET['name']
    else:
        message = ''
    if 'start' in request.GET and request.GET['start']:
        start = int(request.GET['start'])
    else:
        start = 0
    result = utils.semantic.search(message, start)
    return render(request, 'search/paper.html', {'key': message, 'total': result[0], 'articles': result[1]})
    
def author(request, pid):
    author = utils.dblp.gen_author(pid)
    mxyear, mnyear = time.localtime(time.time()).tm_year, 0
    pubcnt, node, link = {}, {}, set()
    idx, ridx = {}, {}
    url = {}
    for i, pub in enumerate(author.publications):
        if 'ee' not in pub:
            pub['ee'] = "/"
        if 'key' not in pub:
            pub['key'] = ""
        author.publications[i]['url'] = '<a href=\'' + pub['ee'] + '\'>' + pub['title'] + '</a>'
        if pub['ee']!="":
            author.publications[i]['doi'] = pub['ee'].split('/')[-2] + '/' + pub['ee'].split('/')[-1]
        else:
            author.publications[i]['doi'] = ""
        year = int(pub['year'])
        mnyear = year
        if year > mxyear:
            mxyear = year
        if year in pubcnt:
            pubcnt[year] += 1
        else:
            pubcnt[year] = 1
        for coauthor in pub['author']:
            url[coauthor[1]] = coauthor[0]
            if coauthor[1] not in node:
                node[coauthor[1]] = 0
            node[coauthor[1]] += 1
            for coauthor2 in pub['author']:
                a, b = coauthor[1], coauthor2[1]
                if a > b: a, b = b, a
                if (a, b) not in link:
                    link.add((a, b))
    for i in range(mnyear, mxyear + 1):
        if i not in pubcnt:
            pubcnt[i] = 0

    from pyecharts import options as opts
    from pyecharts.charts import Bar
    bar = (
        Bar(init_opts=opts.InitOpts(width="300px", height="280px"))
            .add_xaxis(list(range(mnyear, mxyear + 1)))
            .add_yaxis("count", [pubcnt[year] for year in range(mnyear, mxyear + 1)])
            # .set_global_opts(title_opts=opts.TitleOpts(title="publications"))
            .render('static/publish.html')
    )

    import numpy as np
    from communities.algorithms import louvain_method
    node_sort = sorted(node.items(), key=lambda p: -p[1])
    node.clear()
    num = 0
    for (key, value) in node_sort:
        idx[key] = num
        ridx[num] = key
        node[key] = value
        num += 1
        if num>=50: # show 30 related person
            break
    adj_matrix = np.zeros((num, num))
    for (u, v) in iter(link):
        if u in idx and v in idx:
            adj_matrix[idx[u]][idx[v]] = 1
    communities, _ = louvain_method(adj_matrix)
    category = {}
    for id, community in enumerate(communities):
        for authorid in community:
            category[ridx[authorid]] = id  

    from pyecharts.charts import Graph
    from math import log, ceil
    nodes = []
    for key, value in node.items():
        size = ceil(log(value/int(author.papers)*100))
        node[key] = size
        if size>=1:
            nodes.append(opts.GraphNode(name=key, symbol_size=size*8, value=value, category=category[key]))
    links = []
    for edge in link:
        if edge[0] in idx and edge[1] in idx and node[edge[0]]>=1 and node[edge[1]]>=1:
            links.append(opts.GraphLink(source=edge[0], target=edge[1]))
    
    categories = []
    for i in range(len(category)):
        categories.append({"symbol": "circle"})

    c = (
        Graph(init_opts=opts.InitOpts(width="300px", height="280px"))
            .add("", nodes, links, categories=categories, repulsion=100, is_draggable=True)
            # .set_global_opts(title_opts=opts.TitleOpts(title="co-author"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .render('static/coauthor.html')
    )

    coauthor = []
    cnt = 0
    for (key, value) in node_sort:
        if cnt>5:
            break
        if cnt!=0:
            coauthor.append([url[key], value])
        cnt += 1
    return render(request, 'search/author/detail.html', {'author': author, 'coauthor': coauthor})

def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h  = randint(0,100)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)

def article(request, doi):
    article = utils.semantic.genArticle(doi)
    if article.error:
        return HttpResponse(article.error)
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    citcnt = {}
    mnyear, mxyear = time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_year
    for citation in article.citations:
        year = citation['year']
        if year==None:
            continue
        if year < mnyear:
            mnyear = year
        if year > mxyear:
            mxyear = year
        if year not in citcnt:
            citcnt[year] = 1
        else:
            citcnt[year] += 1
    for i in range(mnyear, mxyear + 1):
        if i not in citcnt:
            citcnt[i] = 0
    bar = (
        Bar(init_opts=opts.InitOpts(width="400px", height="300px"))
            .add_xaxis(list(range(mnyear, mxyear + 1)))
            .add_yaxis("count", [citcnt[year] for year in range(mnyear, mxyear + 1)],
                       itemstyle_opts=opts.ItemStyleOpts(color="blue"))
            .set_global_opts(title_opts=opts.TitleOpts(title="citations"))
            .render('static/citation.html')
    )

    keywords = []

    from wordcloud import WordCloud
    if article.abstract!=None:
        WordCloud( background_color=None,
            mode="RGBA",  
            width=400,
            height=300,
            collocations=True,
            color_func = random_color_func,
            ).generate(article.abstract).to_file('static/images/word.png')
        import RAKE.rake
        keywords = RAKE.rake.getkey(article.title+'.'+article.abstract)
    return render(request, 'search/paper/detail.html', {'article': article, 'keywords': keywords})
