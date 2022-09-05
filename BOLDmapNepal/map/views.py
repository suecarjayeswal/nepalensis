from audioop import add
from turtle import color
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search, Listing
import folium
import geocoder
from .forms import SearchForm
import pandas as pd
import os
import numpy as np
import branca
from pathlib import Path
from folium.plugins import MarkerCluster,HeatMap
from pathlib import Path
from .filters import ListingFilter
import re
from fuzzywuzzy import fuzz

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

filepath = os.path.join(BASE_DIR,"data files","bold_data2.csv")
filepath2 = os.path.join(BASE_DIR,"data files","bold_data.tsv")
df = pd.read_csv(filepath)
ldf = pd.read_csv(filepath2,delimiter='\t')
def popup_html(row,dft=pd.DataFrame()):
    i = row
    if not dft.empty:
        df = dft
    else:
        df = pd.read_csv(filepath)
    #print("inside dft2",row,df)
    queries = ['processid','sampleid','phylum_name','class_name','order_name','family_name','genus_name','species_name','subspecies_name']
    genus_name = df['genus_name'].iloc[i]
    species_name = df['species_name'].iloc[i]
    imgurl = df['image_urls'].iloc[i]
    name = str(genus_name)+ " " + str(species_name)
    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    html1 = """ <html><head><h4 style="margin-bottom:10"; width="200px"display: 'flex';align-items: 'center';justify-content: 'space-between';>{}""".format("Info")
    html2=""
    # #print(imgurl)
    # if str(imgurl) != 'nan':
    #     html2 = html2+ """<img src={} height = '100' width='100'>""".format(imgurl)
    html2= """</h4></head><table style="height: 126px; width: 350px;"><tbody><tr><td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">{}</span>""".format("name")+"""</td><td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(name) 
    
    html2 = html2+ """</tr>"""
    for that in queries:
        html2 = html2+"""<tr><td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">{}</span>""".format(that)+"""</td><td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(df[that].iloc[i]) + """</tr>"""
    hyperlink = "https://www.boldsystems.org/index.php/Public_RecordView?processid={}".format(df['processid'].iloc[i])
    html2= html2+ """<tr><td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">{}</span>""".format("More Info")+"""</td><td style="width: 150px;background-color: """+ right_col_color +""";"><a href={}>here</a></td>""".format(hyperlink) + """</tr>"""
    html3 = """</tbody></table></html>"""
    html = html1 + html2 + html3
    return html

def getHeaders(filename):
    file = open(filename,"r")
    for line in file:
        headers = line.split('\t')
        break
    return headers
def getlocs(filename): 
    df = pd.read_csv(filename)
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
def finder(crit,value):
    #(ldf[i].str.contains(j, flags=re.I, regex=True))   for i,j in zip(crit,value)
    #conditions = [ ldf[i]==j for i,j in zip(crit,value)]
    #fuzz.ratio(Str1.lower(),Str2.lower())
    conditions = [ ]
    for i,j in zip(crit,value):
        tmp = (ldf[i].str.contains(j, flags=re.I, regex=True)) 
        tmp[tmp!=True] = False
        conditions.append(tmp)
    tempdf = ldf.loc[np.bitwise_and.reduce(conditions)]
    conditions = [tempdf['lat'].isnull(),tempdf['lon'].isnull()]
    tempdf.loc[np.bitwise_and.reduce(conditions),['lat','lon']]=[27.7172,85.3240]
    print(tempdf.reset_index())
    return tempdf.reset_index()


# Create your views here.
def index(request):
    #address = request.POST.get('address')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()

    
    # listings = Listing.objects.all()
    # listing_filter = ListingFilter(request.GET,queryset=listings)
    
    address = Search.objects.all().last()
    address = str(address)
    if address.find('=') != -1:
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
        if crit:
            tempdf = finder(crit,value)
            popupslis=[]
            locs=[]
            #print("after crit",tempdf)
            for i,row in tempdf.iterrows():
                html = popup_html(i,tempdf)
                locs.append([row['lat'],row['lon']])
                popup = folium.Popup(folium.Html(html, script=True), max_width=500)
                popupslis.append(popup)
            if not tempdf.empty: 
                m = folium.Map(location=[27.79,85.2714],zoom_start=6,)
                folium.TileLayer(tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr = 'Esri',name = 'Esri Satellite',overlay = True,opacity=0.6,control = True).add_to(m)
                HeatMap(locs,min_opacity=0.1,control=True, blur = 35).add_to(m)
                MarkerCluster(locs,popups=popupslis).add_to(m)
                m = m._repr_html_()
                context = {
                    'm':m,
                    'form':form,
                    # 'listing_filter':listing_filter,
                }
                return render(request,'index.html',context)
    
    print("not run",address)
    address = Search.objects.all().last()
    location =  geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None :
        address.delete()
        return HttpResponse('Your Input is invalid')
    #creating map object
    m = folium.Map(location=[27.79,85.2714],zoom_start=6,)
    folium.TileLayer(tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr = 'Esri',name = 'Esri Satellite',overlay = True,opacity=0.6,control = True).add_to(m)
    folium.Marker([lat,lng],tooltip='Click for More',popup=country, icon=folium.Icon(color="red")).add_to(m)
    
    
    df3 = pd.read_csv(os.path.join(BASE_DIR,"data files","populus.csv"))
    flocs = df3.loc[:,'locs']
    popups = df3.loc[:,'popups']
    locs = []
    for a in flocs:
        b,c = ((a)[1:-1].split(','))
        locs.append([float(b),float(c)])
    popupslis=popups
       
    # locs = getlocs(filepath)
    # for i in range(0,len(df)):
    #     html = popup_html(i)
    #     iframe = branca.element.IFrame(html=html,width=510,height=280)
    #     popup = folium.Popup(folium.Html(html, script=True), max_width=500)
    #     popupslis.append(popup)
    HeatMap(locs,min_opacity=0.1,control=True, blur = 35).add_to(m)
    MarkerCluster(locs,popups=list(popupslis)).add_to(m)
    m = m._repr_html_()
    context = {
        'm':m,
        'form':form,
        # 'listing_filter':listing_filter,
    }
    return render(request,'index.html',context)
    