from django.http import HttpResponse
from django.shortcuts import render, redirect
from pyecharts import options as opts
from pyecharts.charts import Bar
import dblp.work
def page(request):
    return render(request, 'search.html')

def search(request):
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        message = request.GET['name']
    else:
        message = ''
    return render(request, 'result.html', {'authors': dblp.work.search(message)})
    
def author(request, pid):
    author = dblp.work.gen_author(pid)
    mxyear, mnyear = 0, 0
    pubcnt = {}
    for i, pub in enumerate(author.publications):
        if not ('ee' in pub):
            pub['ee'] = ""
        author.publications[i]['url'] = '<a href=\'' + pub['ee'] + '\'>' + pub['title'] + '</a>'
        year = int(pub['year'])
        if i==0: 
            mxyear = year
        mnyear = year
        if year in pubcnt:
            pubcnt[year] += 1
        else:
            pubcnt[year] = 1
    for i in range(mnyear, mxyear+1):
        if not (i in pubcnt):
            pubcnt[i] = 0
    from pyecharts import options as opts
    from pyecharts.charts import Bar
    bar=(
        Bar()
        .add_xaxis(list(range(mnyear, mxyear+1)))
        .add_yaxis("count", [pubcnt[year] for year in range(mnyear, mxyear+1)])
        .set_global_opts(title_opts=opts.TitleOpts(title="publications"))
    )
    bar.render('static/tmp.html')
    return render(request, 'author.html', {'author': author})