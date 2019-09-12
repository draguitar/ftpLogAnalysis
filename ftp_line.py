# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:44:39 2019

@author: C09700
"""

from pyecharts.charts import Line
from pyecharts import options as opts

from pyecharts.options import InitOpts

from sklearn import preprocessing 

import pandas as pd


log_data = pd.read_csv("./new_data_download.csv")
df = pd.DataFrame(log_data)


df['dateTime'] = df['date']+' '+df['time']

line = (
        Line()
        .add_xaxis(
                df['dateTime'].tolist()
            
        )
        .add_yaxis(
                "下載", 
                df['download'],
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average",name="平均值")])
        )
        .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
                label_opts=opts.LabelOpts(is_show=False)#顯示資料點
        )
        .set_global_opts(
                title_opts=opts.TitleOpts(title="FTP流量分析"),
                toolbox_opts=opts.ToolboxOpts(),
                datazoom_opts=opts.DataZoomOpts(),
                
                
                xaxis_opts=opts.AxisOpts(
                    name="日期",
                    splitline_opts=opts.SplitLineOpts(is_show=True)     
                ),
                
                yaxis_opts=opts.AxisOpts(
                    type_="log",
                    name="秒",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    is_scale=True
                ),
                #交點輔助線        
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    trigger= 'axis',                          
                ),               
        )
)

line.render()




#line = (
#        Line()
#        .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
#        .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
#        .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
#        .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
#)
#
#line.render()
