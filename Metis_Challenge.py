# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:04:52 2018

@author: willi
"""
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 14:26:46 2018

@author: willi
"""


from datetime import datetime, timedelta
import matplotlib.dates as mdates
import csv
import json

import scipy
print('scipy: %s' % scipy.__version__)
# numpy
import numpy as np
print('numpy: %s' % np.__version__)
# matplotlib
import matplotlib.pyplot as plt
import matplotlib as mtl
print('matplotlib: %s' % mtl.__version__)
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
# pandas
import pandas
print('pandas: %s' % pandas.__version__)
# statsmodels
import statsmodels
print('statsmodels: %s' % statsmodels.__version__)
# scikit-learn


from pandas.plotting import scatter_matrix
years=mdates.YearLocator()
months=mdates.MonthLocator()
yearsFmt=mdates.DateFormatter('%Y')



url="https://data.townofcary.org/api/v2/catalog/datasets/rdu-weather-history/exports/json"
dataset = pandas.read_json(url)
data_pd=pandas.DataFrame(dataset)

print("\n\n")
print("In the following we analyze a dataset for weather in Cary, NC"+\
      "spanning October 3, 2009 to May 25, 2018 or 4,166 days. The data" \
      " consists of 4166 entries with 28 attributes, including date." \
      "The attributes are as follows:")
print("")
print(list(data_pd.keys()))

print("\n\n")
print("It is convenient to focus on the numeric entries.  We also drop" \
      "some numeric attributes since they are 'uninteresting' i.e, "\
      "they don't correlate stronly with the other variables.  This" \
      "will also make the analysis easier, since otherwise there is "
      "too much to visualize at once.\n")

print("The dropped variables are:\n")
drp=['thunder','rain','mist','smokehaze','snow','blowingsnow', \
                         'fog','drizzle','dust','hail','freezingrain','glaze',\
                         'fogground','fogheavy','freezingfog','highwind','ice',\
                          'fastest2minwinddir']
print(drp)


data_small=data_pd.drop(drp,axis=1)

print("\n In our reduced dataset, the first 5 rows look like:\n")

print(data_small.head(5))

print("\n\n")

print("Below is a brief overview of the data:")
print(data_small.describe())

print("\n\n")

print("Now, let's plot some histograms of the data.\n\n")

data_small.hist(xlabelsize=1,ylabelsize=1); plt.show()

print("\n\nA few comments.  Windspeed and temperatures are much "\
      "more skewed than I was expecting.  At first pass, this "\
      "appears to be statistically significant.  The skew "\
      "towards warmer days may have to do with the difference in "\
      "mechanisms between heating and cooling.  Heating proceeds "\
      "via solar radiation, which is efficient and quick, while " \
      "cooling is more slow.\n\n Another point to note is that the "\
      "histograms for snowfall are worthless since they are completely " \
      "dominated by the days with zero snowfall.  Thus, the snowfall " \
      "will require a more careful analysis.")

print("\n\nBefore proceeding, let's look for correlations in the data. "\
      "Below we plot a scatter matrix.")


scatter_matrix(data_small)
plt.show()

print("\n\n Essentially, we see correlations where expected. " \
      "For intance, a high max temperature corresponds to a high min. " \
      "One strange feature are the apparent strips that appear in "\
      "columns and rows six.  This will be discussed later. " \
      "\n\n First, let's plot the highs and lows:")

t_max=[]; t_min=[]; t_ave=[];

for x in range(len(dataset)-1):
    dt=dataset['date'][x].to_pydatetime()
    tmax=float(dataset['temperaturemax'][x])
    tmin=float(dataset['temperaturemin'][x])
    tave=(tmax+tmin)/2
    if type(tmax)==float:
        t_max.append([dt,tmax])
    if type(tmin)==float:
        t_min.append([dt,tmin])
    if type(tave)==float:
        t_ave.append([dt,tave])

        
       
days=list(range(len(t_max)))
plt.plot(days,[x[1] for x in t_max],'ro',days,[x[1] for x in t_min])
plt.xlabel('Day')
plt.ylabel('Temperature in Farenheit')
plt.show()
  
    

        
max_temp=max(t_max,key=lambda x: x[1])
min_temp=min(t_min,key=lambda x: x[1])
max_ave=max(t_ave,key=lambda x: x[1])
min_ave=min(t_ave,key=lambda x: x[1])

        


#print("")
#print("The hottest day in this period was " \
#       "{}-{}-{} with a high of {} ".format(max_temp[0].year,max_temp[0].month,max_temp[0].day,max_temp[1]) \
#       +"degrees celsius")
print(" ")
for x in t_max:
    if x[1]==max_temp[1]:
        print("Highest high temp of {} on {}-{}-{}".format(x[1],x[0].year,x[0].month,x[0].day))
print(" ")
for x in t_ave:
    if x[1]==max_ave[1]:
        print("High average temp of {} on {}-{}-{}".format(x[1],x[0].year,x[0].month,x[0].day))

print("")
for x in t_min:
    if x[1]==min_temp[1]:
        print("Lowest low temp of {} on {}-{}-{}".format(x[1],x[0].year,x[0].month,x[0].day))

print("")
for x in t_ave:
    if x[1]==min_ave[1]:
        print("Low average temp of {} on {}-{}-{}".format(x[1],x[0].year,x[0].month,x[0].day))






#Note that the max/min function only returns the first instance of a 
#maximum.  Therefore, we should in principle worry abou the possibility
#of multiple days with the same max/min temperatures.  To check
#that this does not happen we include the following test:

for x in t_max:
    if t_max[1]==max_temp[1]:
        print(t_max[0])
        
for x in t_ave:
    if t_max[1]==max_temp[1]:
        print(t_max[0])

for x in t_min:
    if t_min[1]==min_temp[1]:
        print(t_min[0])


print("\n Now we return to the snow depth.  Let's filter out the "\
      "zero entries (and the occasional 'None') entry. A histogram "\
      "of the remaining data looks like:")
    
#First, we filter out the zero and 'none' entries

snow=[]
for i in range(len(dataset)-1):
    sd=float(dataset['snowdepth'][i])
    if sd != 0:
        snow.append(sd)
snow2=[x for x in snow if str(x) != 'nan']

binning=[6/100*x for x in range(101)]
plt.hist(snow2,binning)
plt.show()

print("\n One sees somewhat discreet values, which is not what " \
      "we would expect at all in the real world.  Apparently what "\
      "is happening is that meteorologist are using some unit like " \
      "an inch to measure the snow and then rounding off.  However, "\
      "this does not explain why some of the lines appear to be split. "\
      "Perhaps this could be explained if these were measured in inches, "\
      "and then converted to centimeters, with some inconsistency in the "\
      "rounding procedure?  In any case, this is a systematic distortion "\
      "of the data caused by the practice of meteorologist.")


#Convert pandas dateframe to a ndarray
array=data_small.values


