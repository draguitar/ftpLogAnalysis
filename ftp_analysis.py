# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# 檔案大小103720kb
#

# +
from sklearn import preprocessing 

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import logging

# +
from datetime import datetime

def date2DayOfWeek(s) :
    DayOfWeek = datetime.strptime(s, "%Y-%m-%d").weekday() + 1
    return DayOfWeek



# +
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 設定輸出格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger('').addHandler(console)
 
# root 輸出
# logging.info('道可道非常道')

log_data = pd.read_csv("./new_data_download.csv")


# +
df = pd.DataFrame(log_data)

dayOfWeek = []

for d in df.date:
    dayOfWeek.append(date2DayOfWeek(d))

# 新增星期欄位
df['dayOfWeek'] = dayOfWeek

df.to_csv('Result.csv',index=False)

# -

# # # # 將資料分開為 白天、下午、非上班、假日

# +
# 非假日
df_work_day = df[(df['dayOfWeek'] != 6) & (df['dayOfWeek'] != 7) ]

#非假日早上
df_am = df_work_day[(df_work_day['time'] >= '07:15') & (df_work_day['time'] < '13:15')]
df_am.to_csv('df_am.csv',index=False)
# 非假日下午
df_pm = df_work_day[(df_work_day['time'] >= '13:15') & (df_work_day['time'] < '19:15')]
df_pm.to_csv('df_pm.csv',index=False)
# 非假日晚上
df_night_1 = df_work_day[(df_work_day['time'] >= '19:15') & (df_work_day['time'] < '23:59')]

df_night_2 = df_work_day[(df_work_day['time'] < '07:15')]

df_night = df_night_1.append(df_night_2)
df_night.to_csv('df_night.csv',index=False)

# 假日
df_holiday = df[(df['dayOfWeek'] == 6) | (df['dayOfWeek'] == 7) ]

df_holiday.to_csv('df_holiday.csv',index=False)
# -

print('===========平日AM===========')
print(df_am.describe())
print('===========平日PM===========')
print(df_pm.describe())
print('===========平日非上班===========')
print(df_night.describe())
print('===========假日===========')
print(df_holiday.describe())

# +
# 上班時段
df_work_day = df_am.append(df_pm)
df_work_day.describe()

print('===========上班時段===========')
print(df_work_day.describe())


fliter = (df_work_day.download >= 108.685400)
df_work_busy = df_work_day[fliter]
df_work_busy.to_csv('df_work_busy.csv',index=False)

print('{}'.format('================================================='))
count = str(len(df_work_busy))
print("{} {}".format("總忙碌筆數：", count))
# 早上與下午忙碌的分布s
df_am = df_work_busy[(df_work_busy['time'] >= '07:15') & (df_work_busy['time'] < '13:15')]

print("{} {} {:.2f}%".format("白天忙碌筆數：", str(len(df_am))+'/'+ count, len(df_am)/int(count) * 100))
df_pm = df_work_busy[(df_work_busy['time'] >= '13:15') & (df_work_busy['time'] < '19:15')]
print("{} {} {:.2f}%".format("下午忙碌筆數：", str(len(df_pm))+'/'+ count, len(df_pm)/int(count) * 100))

# 週一到週五忙碌分布
print('{}'.format('================================================='))
df_1 = df_work_busy[(df_work_busy['dayOfWeek'] == 1)]
print("{} {} {:.2f}%".format("週一：", str(len(df_1)) + '/' + count, len(df_1)/int(count) * 100))
df_2 = df_work_busy[(df_work_busy['dayOfWeek'] == 2)]
print("{} {} {:.2f}%".format("週二：", str(len(df_2)) + '/' + count, len(df_2)/int(count) * 100))
df_3 = df_work_busy[(df_work_busy['dayOfWeek'] == 3)]
print("{} {} {:.2f}%".format("週三：", str(len(df_3)) + '/' + count, len(df_3)/int(count) * 100))
df_4 = df_work_busy[(df_work_busy['dayOfWeek'] == 4)]
print("{} {} {:.2f}%".format("週四：", str(len(df_4)) + '/' + count, len(df_4)/int(count) * 100))
df_5 = df_work_busy[(df_work_busy['dayOfWeek'] == 5)]
print("{} {} {:.2f}%".format("週五：", str(len(df_5)) + '/' + count, len(df_5)/int(count) * 100))

# +
plt.style.use('ggplot')

plt.title('Downloading Time')

df_1_AM = df_1[(df_1['time'] < '13:15')]
df_1_PM = df_1[(df_1['time'] >= '13:15')]

df_2_AM = df_2[(df_2['time'] < '13:15')]
df_2_PM = df_2[(df_2['time'] >= '13:15')]

df_3_AM = df_3[(df_3['time'] < '13:15')]
df_3_PM = df_3[(df_3['time'] >= '13:15')]

df_4_AM = df_4[(df_4['time'] < '13:15')]
df_4_PM = df_4[(df_4['time'] >= '13:15')]

df_5_AM = df_5[(df_5['time'] < '13:15')]
df_5_PM = df_5[(df_5['time'] >= '13:15')]

x = ['Mon', 'Tue', 'Wed', 'Thir', 'Fri']

class_a = [len(df_1_AM), len(df_2_AM), len(df_3_AM), len(df_4_AM), len(df_5_AM)]
class_b = [len(df_1_PM), len(df_2_PM), len(df_3_PM), len(df_4_PM), len(df_5_PM)]

plt.bar(x, class_a, label = 'am', align = "edge", width = -0.3)
plt.bar(x, class_b, label = 'pm', align = "edge", width = 0.3)
plt.legend() #要使用label要加這行
# -

# # 柱狀圖

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
x = ['Mon', 'Tue', 'Wed', 'Thir', 'Fri']
class_a = [17, 22, 16, 4, 7]
plt.bar(x, class_a, label = 'class_a', width = 0.4)

labels = ['morning', 'afternoon']
size = [46.97, 53.03]
plt.pie(size , labels = labels,autopct='%1.1f%%')
plt.axis('equal')
plt.show()

# +
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


x_axix = df_work_day.date + df_work_day.time
train_acys = df_work_day.download

sub_axix = filter(lambda x:x%200 == 0, x_axix)
plt.title('FTP LOG Analysis')

plt.plot(x_axix, train_acys, color='green', label='Download_time')

plt.legend() # 显示图例
plt.xlabel('Date')
plt.ylabel('Downloading time')
plt.show()
#python 一个折线图绘制多个曲线
# -

# # Uploading Report

log_data = pd.read_csv("./new_data_upload.csv")

# +
df = pd.DataFrame(log_data)

dayOfWeek = []

for d in df.date:
    dayOfWeek.append(date2DayOfWeek(d))

# 新增星期欄位
df['dayOfWeek'] = dayOfWeek

df.to_csv('Result_upload.csv',index=False)

# +
# 非假日
df_work_day = df[(df['dayOfWeek'] != 6) & (df['dayOfWeek'] != 7) ]

#非假日早上
df_am = df_work_day[(df_work_day['time'] >= '07:15') & (df_work_day['time'] < '13:15')]
df_am.to_csv('df_am_upload.csv',index=False)
# 非假日下午
df_pm = df_work_day[(df_work_day['time'] >= '13:15') & (df_work_day['time'] < '19:15')]
df_pm.to_csv('df_pm_upload.csv',index=False)
# 非假日晚上
df_night_1 = df_work_day[(df_work_day['time'] >= '19:15') & (df_work_day['time'] < '23:59')]

df_night_2 = df_work_day[(df_work_day['time'] < '07:15')]

df_night = df_night_1.append(df_night_2)
df_night.to_csv('df_night_upload.csv',index=False)

# 假日
df_holiday = df[(df['dayOfWeek'] == 6) | (df['dayOfWeek'] == 7) ]

df_holiday.to_csv('df_holiday_upload.csv',index=False)
# -

print('===========平日AM===========')
print(df_am.describe())
print('===========平日PM===========')
print(df_pm.describe())
print('===========平日非上班===========')
print(df_night.describe())
print('===========假日===========')
print(df_holiday.describe())

# +
# 上班時段
df_work_day = df_am.append(df_pm)
df_work_day.describe()

print('===========上班時段===========')
print(df_work_day.describe())


fliter = (df_work_day.upload >= 537.436500)
df_work_busy = df_work_day[fliter]
df_work_busy.to_csv('df_work_busy_upload.csv',index=False)

print('{}'.format('================================================='))
count = str(len(df_work_busy))
print("{} {}".format("總忙碌筆數：", count))
# 早上與下午忙碌的分布s
df_am = df_work_busy[(df_work_busy['time'] >= '07:15') & (df_work_busy['time'] < '13:15')]

print("{} {} {:.2f}%".format("白天忙碌筆數：", str(len(df_am))+'/'+ count, len(df_am)/int(count) * 100))
df_pm = df_work_busy[(df_work_busy['time'] >= '13:15') & (df_work_busy['time'] < '19:15')]
print("{} {} {:.2f}%".format("下午忙碌筆數：", str(len(df_pm))+'/'+ count, len(df_pm)/int(count) * 100))

# 週一到週五忙碌分布
print('{}'.format('================================================='))
df_1 = df_work_busy[(df_work_busy['dayOfWeek'] == 1)]
print("{} {} {:.2f}%".format("週一：", str(len(df_1)) + '/' + count, len(df_1)/int(count) * 100))
df_2 = df_work_busy[(df_work_busy['dayOfWeek'] == 2)]
print("{} {} {:.2f}%".format("週二：", str(len(df_2)) + '/' + count, len(df_2)/int(count) * 100))
df_3 = df_work_busy[(df_work_busy['dayOfWeek'] == 3)]
print("{} {} {:.2f}%".format("週三：", str(len(df_3)) + '/' + count, len(df_3)/int(count) * 100))
df_4 = df_work_busy[(df_work_busy['dayOfWeek'] == 4)]
print("{} {} {:.2f}%".format("週四：", str(len(df_4)) + '/' + count, len(df_4)/int(count) * 100))
df_5 = df_work_busy[(df_work_busy['dayOfWeek'] == 5)]
print("{} {} {:.2f}%".format("週五：", str(len(df_5)) + '/' + count, len(df_5)/int(count) * 100))

# +
plt.style.use('ggplot')

plt.title('Uploading Time')

df_1_AM = df_1[(df_1['time'] < '13:15')]
df_1_PM = df_1[(df_1['time'] >= '13:15')]

df_2_AM = df_2[(df_2['time'] < '13:15')]
df_2_PM = df_2[(df_2['time'] >= '13:15')]

df_3_AM = df_3[(df_3['time'] < '13:15')]
df_3_PM = df_3[(df_3['time'] >= '13:15')]

df_4_AM = df_4[(df_4['time'] < '13:15')]
df_4_PM = df_4[(df_4['time'] >= '13:15')]

df_5_AM = df_5[(df_5['time'] < '13:15')]
df_5_PM = df_5[(df_5['time'] >= '13:15')]

x = ['Mon', 'Tue', 'Wed', 'Thir', 'Fri']

class_a = [len(df_1_AM), len(df_2_AM), len(df_3_AM), len(df_4_AM), len(df_5_AM)]
class_b = [len(df_1_PM), len(df_2_PM), len(df_3_PM), len(df_4_PM), len(df_5_PM)]

plt.bar(x, class_a, label = 'am', align = "edge", width = -0.3)
plt.bar(x, class_b, label = 'pm', align = "edge", width = 0.3)
plt.legend() #要使用label要加這行

# -

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
x = ['Mon', 'Tue', 'Wed', 'Thir', 'Fri']
class_a = [19, 17, 16, 6, 6]
plt.bar(x, class_a, label = 'class_a', width = 0.4)

labels = ['morning', 'afternoon']
size = [45.31, 54.69]
plt.pie(size , labels = labels,autopct='%1.1f%%')
plt.axis('equal')
plt.show()

# +
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


x_axix = df_work_day.date + df_work_day.time
train_acys = df_work_day.upload

sub_axix = filter(lambda x:x%200 == 0, x_axix)
plt.title('FTP LOG Analysis')

plt.plot(x_axix, train_acys, color='green', label='Upload_time')

plt.legend() # 显示图例
plt.xlabel('Date')
plt.ylabel('Uploading time')
plt.show()
#python 一个折线图绘制多个曲线
