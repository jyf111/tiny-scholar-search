from pyecharts import options as opts
from pyecharts.charts import Bar

bar=(
    Bar()
        .add_yaxis("count", )
        .set_global_opts(title_opts=opts.TitleOpts(title="publications"))
    )

bar.render()