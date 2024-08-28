import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import *

data = pd.read_excel('./B站新榜_综合指数榜单.xlsx')
print(data.head())


# 数据处理
def transform(x):
    x = str(x)
    if 'w' in x:
        return round(float(x.split('w')[0]), 2)
    elif '亿' in x:
        x = round(float(x.split('亿')[0]) * 10000, 2)
        return x
    else:
        x = round(float(x) / 10000, 2)
        return x


def transform_a(x):
    x = str(x)
    if 'w' in x:
        return round(float(x.split('w')[0]) * 10000, 2)
    else:
        x = round(float(x), 2)
        return x


data['弹幕数'] = data['弹幕数'].apply(lambda x: transform(x))
data['获赞数'] = data['获赞数'].apply(lambda x: transform(x))
data['播放数'] = data['播放数'].apply(lambda x: transform(x))
data['涨粉数'] = data['涨粉数'].apply(lambda x: transform(x))
data['投币数'] = data['投币数'].apply(lambda x: transform(x))
data['投稿视频数'] = data['投稿视频数'].apply(lambda x: transform(x))

data.rename(columns={"弹幕数": '弹幕数/w', "获赞数": '获赞数/w', "播放数": '播放数/w', "涨粉数": '涨粉数/w',
                     "投币数": '投币数/w'}, inplace=1)

data = data[
    ['排名', '性别', '类型', '投稿视频数', 'up主', 'up主标签', '创作领域', '等级', '投币数/w', '弹幕数/w', '获赞数/w',
     '播放数/w', '涨粉数/w', '榜单类型', '时间']]

print(data.head())

numerical_data = data.select_dtypes(include=[np.number])

rows = numerical_data.corr().index.size
cols = numerical_data.corr().columns.size

data_ = []
data_ = [[i, j, round(float(numerical_data.corr().iloc[i, j]), 3) or '-'] for i in range(rows) for j in range(cols)]

c = (
    HeatMap(init_opts=opts.InitOpts(width='1080px', theme="light"))
    .add_xaxis(numerical_data.corr().index.tolist())
    .add_yaxis(
        "相关系数",
        numerical_data.corr().columns.tolist(),
        data_,
        label_opts=opts.LabelOpts(is_show=True, position="inside"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="相关系数热力图",
            subtitle='数据来源：新站',
            pos_left='center'),
        legend_opts=opts.LegendOpts(
            is_show=False
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True,
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=1
                )
            ),
            axislabel_opts=opts.LabelOpts(
                rotate=90,
                font_size=12
            ),
            interval=0
        ),
        yaxis_opts=opts.AxisOpts(
            name='',
            type_="category",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True,
                areastyle_opts=opts.AreaStyleOpts(
                    opacity=1
                )
            ),
            axislabel_opts=opts.LabelOpts(
                font_size=12
            ),
            interval=0
        ),
        visualmap_opts=opts.VisualMapOpts(
            min_=-1,
            max_=1,
            is_calculable=True,
            pos_left='right',
        ),
    )
)
c.render('相关系数热力图.html')


def bar_chart(desc, title_pos, date):
    if date == '03' and '涨粉' in desc:
        esc = '网站估计未统计'
    else:
        esc = ''

    data_month = data[(data['榜单类型'] == '月榜') & (data['时间'] == f'2022-{date}-01')]
    df_t = data_month.sort_values(desc, ascending=False).head(5)
    df_t = df_t.round(2)
    chart = Bar()
    chart.add_xaxis(
        df_t['up主'].tolist()
    )
    chart.add_yaxis(
        '',
        df_t[desc].tolist()
    )

    chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            is_scale=True,
            axislabel_opts={'rotate': '90'},
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                    type_='dashed'
                )
            )
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            name='',
            type_='value',
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                    type_='dashed'
                )
            )
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger='axis',
            axis_pointer_type='shadow'
        ),
        title_opts=opts.TitleOpts(
            title='up主-' + desc,
            subtitle=f'{date.replace("0", "")}月👇👇👇👇 {esc}',
            pos_left=title_pos[0],
            pos_top=title_pos[1],
            title_textstyle_opts=opts.TextStyleOpts(
                color='#00BFFF',
                font_size=16
            )
        )
    )
    return chart


def bar_chart_type(desc, title_pos, date):
    data_month = data[(data['榜单类型'] == '月榜') & (data['时间'] == f'2022-{date}-01')]
    df_t = data.groupby('创作领域').agg({desc: 'sum'}).reset_index()
    df_t = df_t.round(2)
    chart = Bar()
    chart.add_xaxis(
        df_t['创作领域'].tolist()
    )
    chart.add_yaxis(
        '',
        df_t[desc].tolist()
    )
    chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            is_scale=True,
            axislabel_opts={'rotate': '90'},
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                    type_='dashed'
                )
            )
        ),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            name='',
            type_='value',
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                    type_='dashed'
                )
            )
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger='axis',
            axis_pointer_type='shadow'
        ),
        title_opts=opts.TitleOpts(
            title='up主-' + desc,
            subtitle=f'{date.replace("0", "")}月👇👇👇👇 {desc}',
            pos_left=title_pos[0],
            pos_top=title_pos[1],
            title_textstyle_opts=opts.TextStyleOpts(
                color='#00BFFF',
                font_size=16
            )
        )
    )
    return chart


grid = Grid(
    init_opts=opts.InitOpts(
        width='1000px',
        height='2000px',
        theme='light'
    )
)
grid.add(
    bar_chart('投稿视频数', ['5%', '1%'], '04'),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='5%',
        pos_left='5%',
        pos_right='70%',
        pos_bottom='85%'
    )
)
grid.add(
    bar_chart('投币数/w', ['37%', '1%'], '04'),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='5%',
        pos_bottom='85%',
        pos_left='37%',
        pos_right='37%'
    )
)
grid.add(
    bar_chart('弹幕数/w', ['71%', '1%'], '04'),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='5%',
        pos_bottom='85%',
        pos_left='71%',
        pos_right='5%'
    )
)
grid.add(
    bar_chart('获赞数/w', ['5%', '21%'], '04'),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='25%',
        pos_bottom='65%',
        pos_left='5%',
        pos_right='70%'
    )
)
grid.add(
    bar_chart('播放数/w', ['37%', '21%'], '04'),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='25%',
        pos_bottom='65%',
        pos_left='37%',
        pos_right='37%'
    )
)
grid.add(
    bar_chart('涨粉数/w', ['71%', '21%'], '04'),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='25%',
        pos_bottom='65%',
        pos_left='71%',
        pos_right='5%'
    )
)

grid.render('4月数据图.html')

grid_3 = Grid(
    init_opts=opts.InitOpts(
        theme='white',
        width='1000px',
        height='1000px'
    )
)
grid_3.add(
    bar_chart('投稿视频数', ['5%', '1%'], "03"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='8%',
        pos_bottom='73%',
        pos_left='5%',
        pos_right='70%'
    )
)
grid_3.add(
    bar_chart('投币数/w', ['37%', '1%'], "03"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='8%',
        pos_bottom='73%',
        pos_left='37%',
        pos_right='37%'
    )
)
grid_3.add(
    bar_chart('弹幕数/w', ['71%', '1%'], "03"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='8%',
        pos_bottom='73%',
        pos_left='71%',
        pos_right='5%'
    )
)
grid_3.add(
    bar_chart('获赞数/w', ['5%', '42%'], "03"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='50%',
        pos_bottom='28%',
        pos_left='5%',
        pos_right='70%'
    )
)
grid_3.add(
    bar_chart('播放数/w', ['37%', '42%'], "03"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='50%',
        pos_bottom='28%',
        pos_left='37%',
        pos_right='37%'
    )
)
grid_3.add(
    bar_chart('涨粉数/w', ['71%', '42%'], "03"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='50%',
        pos_bottom='28%',
        pos_left='71%',
        pos_right='5%'
    )
)

grid_3.render('3月数据图.html')

grid_2 = Grid(
    init_opts=opts.InitOpts(
        theme='white',
        width='1000px',
        height='1000px'
    )
)
grid_2.add(
    bar_chart('投稿视频数', ['5%', '1%'], "02"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='8%',
        pos_bottom='73%',
        pos_left='5%',
        pos_right='70%'
    )
)
grid_2.add(
    bar_chart('投币数/w', ['37%', '1%'], "02"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='8%',
        pos_bottom='73%',
        pos_left='37%',
        pos_right='37%'
    )
)
grid_2.add(
    bar_chart('弹幕数/w', ['71%', '1%'], "02"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='8%',
        pos_bottom='73%',
        pos_left='71%',
        pos_right='5%'
    )
)
grid_2.add(
    bar_chart('获赞数/w', ['5%', '42%'], "02"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='50%',
        pos_bottom='28%',
        pos_left='5%',
        pos_right='70%'
    )
)
grid_2.add(
    bar_chart('播放数/w', ['37%', '42%'], "02"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='50%',
        pos_bottom='28%',
        pos_left='37%',
        pos_right='37%'
    )
)
grid_2.add(
    bar_chart('涨粉数/w', ['71%', '42%'], "02"),
    is_control_axis_index=False,
    grid_opts=opts.GridOpts(
        pos_top='50%',
        pos_bottom='28%',
        pos_left='71%',
        pos_right='5%'
    )
)

grid_2.render('2月数据图.html')
