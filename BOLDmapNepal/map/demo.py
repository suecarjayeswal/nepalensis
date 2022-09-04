import pandas as pd
import os
import numpy as np
from folium.plugins import HeatMap
import folium


def getHeaders(filename):
    file = open(filename,"r")
    for line in file:
        headers = line.split('\t')
        break
    return headers
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
headers = getHeaders(filepath)
locs = getlocs(filepath)
ldf =  pd.read_csv(filepath, delimiter='\t')
m = folium.Map(location=[27.79,85.2714],zoom_start=6)
for a in locs:
    print(a)
HeatMap(locs).add_to(m)