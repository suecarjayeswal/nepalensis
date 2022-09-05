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

def finder(crit,value):
    conditions = [ ldf[i]==j for i,j in zip(crit,value)]
    print("test")
    tempdf = ldf.loc[np.bitwise_and.reduce(conditions)]
    conditions = [tempdf['lat'].isnull(),tempdf['lon'].isnull()]
    tempdf.loc[np.bitwise_and.reduce(conditions),['lat','lon']]=[27.7172,85.3240]
    return tempdf
address= 'species_name=Rungia pectinata,identification_reference=(L.) Nees,'
address = address.split(",")
crit=[]
value=[]
print("split ,",address)
for a in address[:-1]:
    b,c = a.split('=')
    print("split =",b.strip(),c.strip())
    crit.append(b.strip())
    value.append(c.strip())
print(crit,value)
temdf = finder(crit,value)
print(temdf)
locs = []
for i,row in temdf.iterrows():
    locs.append([row['processid'],row['lat'],row['lon']])
print(len(locs))
for a in locs:
    print(a)
#filepath = os.path.join(os.getcwd(),"BOLDmapNepal","data files","bold_data2.csv")
#df2.to_csv(filepath)
#print(headers)