import pandas as pd
import os
import numpy as np
from folium.plugins import HeatMap
import folium
import geocoder

def getlocs(filename): 
    df = pd.read_csv(filename, delimiter='\t')
    df2 = []
    for a in np.concatenate((df[['lat']].values,df[['lon']].values),axis=1):
        b = str(a)[1:-1]
        df2.append(b)
    df2 = set(df2)
    locs = []
    for a in df2:
        a = a.split(' ')
        d=[]
        for c in a:
            try:
                if c != 'nan':
                    d.append(float(c))
            except:
                continue
        if d != []: locs.append(d)
    return locs

filepath = os.path.join(os.getcwd(),"BOLDmapNepal","data files","bold_data.tsv")
locs = getlocs(filepath)
ldf =  pd.read_csv(filepath, delimiter='\t')
headers = ldf.columns.values
df2 = ldf.sort_values(['lat','lon'])
print(df2.loc[:,['processid','lat','lon']])
df2 = df2.dropna(subset=['lat','lon'])
print(df2.loc[:,['processid','lat','lon']])
latlonlis = []
for i,row in df2.iterrows():
    latlonlis.append([row['lat'],row['lon']])
lat = 30.1200
lon = 81.4000
print(df2.loc[df2['lat']==lat ,['processid','lat','lon']])
filepath = os.path.join(os.getcwd(),"BOLDmapNepal","data files","bold_data2.csv")
df2.to_csv(filepath)
#print(headers)