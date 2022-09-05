import pandas as pd
from pathlib import Path
import folium
import branca
import numpy as np
import os
import re
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

filepath = os.path.join(BASE_DIR,"data files","bold_data2.csv") 
df = pd.read_csv(filepath)
def popup_html(row,dft=pd.DataFrame()):
    i = row
    if not dft.empty:
        df = dft
    else:
        df = pd.read_csv(filepath)
    #print("inside dft2",row,df)
    queries = ("""'processid' 'sampleid' 'recordID' 'catalognum' 'fieldnum' 'institution_storing' 'collection_code' 'bin_uri' 'phylum_name' 'class_name' 'order_name' 'family_name'  'subfamily_name' 'genus_name' 'species_name' 'subspecies_name' 'identification_provided_by' 'identification_method' 'identification_reference' 'collectors' 'collectiondate_start' 'collectiondate_end' 'collectiontime' 'collection_note' 'sampling_protocol' 'lifestage' 'sex' 'reproduction' 'habitat' 'associated_specimens' 'associated_taxa' 'extrainfo' 'notes' 'lat' 'lon' 'elev' 'depth' 'country' 'province_state' 'region' 'sector' 'exactsite' 'image_urls' 'captions' 'copyright_holders' 'photographers'""").split(' ')
    genus_name = df['genus_name'].iloc[i]
    species_name = df['species_name'].iloc[i]
    imgurl = df['image_urls'].iloc[i]
    name = str(genus_name)+ " " + str(species_name)
    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    html1 = """ <html><head><h4 style="margin-bottom:10"; width="200px"display: 'flex';align-items: 'center';justify-content: 'space-between';>{}""".format("Info")
    html2=""
    # #print(imgurl)
    if str(imgurl) != 'nan':
        html2 = html2+ """<img src={} height = '100' width='100'>""".format(imgurl)
    html2= """</h4></head><table style="height: 126px; width: 350px;"><tbody><tr><td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">{}</span>""".format("name")+"""</td><td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(name) 
    
    html2 = html2+ """</tr>"""
    for that in queries:
        if that[1:-1]=='':continue
        html2 = html2+"""<tr><td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">{}</span>""".format(that[1:-1])+"""</td><td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(df[that[1:-1]].iloc[i]) + """</tr>"""
    hyperlink = "https://www.boldsystems.org/index.php/Public_RecordView?processid={}".format(df['processid'].iloc[i])
    html2= html2+ """<tr><td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">{}</span>""".format("More Info")+"""</td><td style="width: 150px;background-color: """+ right_col_color +""";"><a href={}>here</a></td>""".format(hyperlink) + """</tr>"""
    html3 = """</tbody></table></html>"""
    html = html1 + html2 + html3
    return html
def getlocs(filename): 
    df = pd.read_csv(filename)
    df2 = []
    for a in np.concatenate((df[['lat']].values,df[['lon']].values),axis=1):
        b = str(a)[1:-1]
        df2.append(b)
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

locs = getlocs(filepath) 
popupslis=[]
for i in range(0,len(df)):
    html = popup_html(i)
    popupslis.append(html)
    popup = folium.Popup(folium.Html(html, script=True), max_width=500)
    
df2 = pd.DataFrame(columns=['locs','popups'])
print(len(locs),len(popupslis))
df2['locs'] = locs
df2['popups'] = popupslis
df2.to_csv("populus.csv",)
# df2 = pd.read_csv("populus.csv")
# flocs = df2.loc[:,'locs']
# popups = df2.loc[:,'popups']
# locs = []
# # for a in popups:
# #     print(a)
# popups=list(popups)
# for a in popups:
# #     print(a,type(a))
# df = pd.read_csv(filepath)
# print(df.columns.values)
# address= 'region=bagmati,'
# address = address.split(",")
# crit=[]
# value=[]
# print("split ,",address)
# for a in address[:-1]:
#     b,c = a.split('=')
#     print("split =",b.strip(),c.strip())
#     crit.append(b.strip())
#     value.append(c.strip())
# print(crit,value)
# #print(pd.unique( df['region'].str.contains('bagmati', flags=re.I, regex=True)  ))
# conditions = [ ]
# for i,j in zip(crit,value):
#     tmp = (df[i].str.contains(j, flags=re.I, regex=True)) 
#     tmp[tmp!=True] = False
#     print(tmp)