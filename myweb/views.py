from django.http import HttpResponse
from django.shortcuts import render, redirect
from pyecharts import options as opts
from pyecharts.charts import Bar
import utils.dblp
import utils.semantic
import time


def page(request):
    return render(request, 'search.html')


def search(request):
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        message = request.GET['name']
    else:
        message = ''
    exact_authors, likely_authors = utils.dblp.search(message)
    return render(request, 'result.html', {'key': message, 'exact_authors': exact_authors, 'likely_authors': likely_authors})


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
        author.publications[i]['doi'] = pub['ee'].split('/')[-2] + '/' + pub['ee'].split('/')[-1]
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
    nodes = []
    for key, value in node.items():
        nodes.append(opts.GraphNode(name=key, symbol_size=value, value=value, category=int(key == author.name)))
    links = []
    for edge in link:
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
    return render(request, 'author.html', {'author': author})


def article(request, doi):
    article = utils.semantic.Article(doi)
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    citcnt = {}
    mnyear, mxyear = time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_year
    for citation in article.citations:
        year = citation['year']
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
        Bar(init_opts=opts.InitOpts(width="300px", height="200px"))
            .add_xaxis(list(range(mnyear, mxyear + 1)))
            .add_yaxis("count", [citcnt[year] for year in range(mnyear, mxyear + 1)],
                       itemstyle_opts=opts.ItemStyleOpts(color="blue"))
            .set_global_opts(title_opts=opts.TitleOpts(title="citations"))
            .render('static/citation.html')
    )
    return render(request, 'article.html', {'article': article})
