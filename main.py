import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

"""
Author: Yaolin Chen
Date: Late June- early July
Contact: yac97@pitt.edu
Content: This is example script dealing with csv file from Crowdtangle
"""
df = pd.read_csv('./Voice_Of_Biafrans.csv')
# print(df)
df.columns = df.columns.str.replace(' ', '')
print(df.head)

timestamp = df["PostCreated"].tolist()
shares = df["Shares"].tolist()
comments = df["Comments"].tolist()
interact = df["TotalInteractions"].tolist()
overperf = df["OverperformingScore"].tolist()


print("___")
abs_months = []
dates = []
for i in range(len(timestamp)):
    t = timestamp[i]
    year =int(t[0:4])
    month = int(t[5:7])
    abs_month = 12*(year-2020)+ month
    dates +=  [ t[0:7] ]
    abs_months += [abs_month]

########## section 1: counts by month #########
dates_set = []
for i in range(4):
    for j in range(12):
        if (i ==3) and (j > 5):
            break
        ym = '2' + str(i) + '-' + str(j+1)
        dates_set += [ym]


plt.figure( figsize= (20,5))
abs_months_set = list(np.arange(1,43))
plt.hist(abs_months,bins = 42, rwidth=0.7)
plt.xticks(abs_months_set, dates_set,rotation=45)

plt.grid(True)
# plt.show()
plt.savefig('./1_over_year_month.png')


########## section 2: pick hottest month 21/8 #########
# id 20-th
hours = []
filter_shares = list(np.zeros((24)))
filter_comments = list(np.zeros((24)))
filter_interact = list(np.zeros((24)))
filter_overperf = list(np.zeros((24)))
for i in range(len(timestamp)):
    t = timestamp[i]
    year =int(t[0:4])
    month = int(t[5:7])
    if (year == 2021) and (month==8):
        h = int(t[11:13])
        hours += [h]
        filter_shares[h] += shares[i]
        filter_comments[h] += comments[i]
        filter_interact[h] += locale.atoi(interact[i])
        filter_overperf[h] += locale.atof((overperf[i]) )



plt.figure( figsize= (20,5))
plt.hist(hours,bins = 24, rwidth=0.7)
plt.grid(True)
plt.xlabel('hour')
plt.ylabel('count')
plt.title('2021-Aug')
plt.savefig('./2_over_hour.png')


########## section 3: common metric to tell scam or not #########
hours_l = list(np.arange(0,24))
plt.figure( )
plt.plot(hours_l,filter_shares,'-o')
plt.plot(hours_l,filter_comments,'-*')
plt.grid(True)
plt.xlabel('hours')
plt.ylabel('metric')
plt.legend(['shares','comments'])
plt.title('2021-Aug')
plt.savefig('./3_over_hour.png')


########## section 4: shares over hours in hottest month #########

plt.figure(  figsize= (10,10) )
plt.subplot(2,1,1)
plt.plot(hours_l,filter_overperf,'-o')
plt.grid(True)
plt.xlabel('hours')
plt.ylabel('overperforming score')

plt.subplot(2,1,2)
plt.plot(hours_l,filter_interact,'-*')
plt.grid(True)
plt.xlabel('hours')
plt.ylabel('interactions')


plt.savefig('./4a_over_hour.png')



plt.figure()
# plt.hist(hours,bins = 24, rwidth=0.7)
plt.scatter(filter_overperf,filter_interact)
plt.grid(True)
plt.xlabel('overperformance score')
plt.ylabel('interaction')
plt.title('2021-Aug')
plt.savefig('./4_scatter_overperf_vs_interact.png')