from django.http import HttpResponse
from django.shortcuts import render, redirect
from pyecharts import options as opts
from pyecharts.charts import Bar
from random import randint
import utils.dblp
import utils.semantic
import time


def page(request):
    return render(request, 'mainpage.html')

def scholarsearch(request):
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        message = request.GET['name']
    else:
        message = ''
    exact_authors, likely_authors = utils.dblp.search(message)

    return render(request, 'scholarsearch.html', {'key': message, 'exact_authors': exact_authors, 'likely_authors': likely_authors})

def papersearch(request):
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        message = request.GET['name']
    else:
        message = ''
    result = utils.semantic.search(message)
    return render(request, 'papersearch.html', {'key': message, 'total': result[0], 'articles': result[1]})
    
def author(request, pid):
    author = utils.dblp.gen_author(pid)
    mxyear, mnyear = time.localtime(time.time()).tm_year, 0
    pubcnt, node, link = {}, {}, set()
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
        Bar(init_opts=opts.InitOpts(width="300px", height="200px"))
            .add_xaxis(list(range(mnyear, mxyear + 1)))
            .add_yaxis("count", [pubcnt[year] for year in range(mnyear, mxyear + 1)])
            .set_global_opts(title_opts=opts.TitleOpts(title="publications"))
            .render('static/publish.html')
    )

    from pyecharts.charts import Graph
    from math import log, ceil
    nodes = []
    for key, value in node.items():
        size = ceil(log(value/int(author.papers)*100))
        node[key] = size
        if size>=1:
            nodes.append(opts.GraphNode(name=key, symbol_size=size*6, value=value, category=int(key==author.name)))
    links = []
    for edge in link:
        if node[edge[0]]>=1 and node[edge[1]]>=1:
            links.append(opts.GraphLink(source=edge[0], target=edge[1]))
    # TODO kmeans ?
    categories = [
        {"symbol": "circle"},
        {"symbol": "circle"},
    ]
    c = (
        Graph(init_opts=opts.InitOpts(width="300px", height="200px"))
            .add("", nodes, links, categories=categories, repulsion=100, is_draggable=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="co-author"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .render('static/coauthor.html')
    )
    return render(request, 'scholar.html', {'author': author})

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
        Bar(init_opts=opts.InitOpts(width="400px", height="200px"))
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
    return render(request, 'paper.html', {'article': article, 'keywords': keywords})
