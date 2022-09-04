from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search
import folium
import geocoder
from .forms import SearchForm
import pandas as pd
import os
import numpy as np
from pathlib import Path
from folium.plugins import MarkerCluster,HeatMap

def popup_html(row):
    i = row
    institution_name=df['INSTNM'].iloc[i] 
    institution_url=df['URL'].iloc[i]
    institution_type = df['CONTROL'].iloc[i] 
    highest_degree=df['HIGHDEG'].iloc[i] 
    city_state = df['CITY'].iloc[i] +", "+ df['STABBR'].iloc[i]                     
    admission_rate = df['ADM_RATE'].iloc[i]
    cost = df['COSTT4_A'].iloc[i]
    instate_tuit = df['TUITIONFEE_IN'].iloc[i]
    outstate_tuit = df['TUITIONFEE_OUT'].iloc[i]

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
<html>

<head>
<h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(institution_name) + """

</head>
    <table style="height: 126px; width: 350px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Institution Type</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(institution_type) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Institution URL</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(institution_url) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">City and State</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(city_state) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Highest Degree Awarded</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(highest_degree) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Admission Rate</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(admission_rate) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Annual Cost of Attendance $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(cost) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">In-state Tuition $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(instate_tuit) + """
</tr>
<tr>
<td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Out-of-state Tuition $</span></td>
<td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(outstate_tuit) + """
</tr>
</tbody>
</table>
</html>
"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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

filepath = os.path.join(BASE_DIR,"data files","bold_data.tsv")
ldf = pd.read_csv(filepath, delimiter='\t')
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
    tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        opacity=0.6,
        control = True
       ).add_to(m)
    folium.Marker([lat,lng],tooltip='Click for More',popup=country).add_to(m)
    locs = getlocs(filepath)
    MarkerCluster(locs).add_to(m)
    HeatMap(locs,min_opacity=0.1,control=True, blur = 35).add_to(m)
    # for a in locs:
    #     try:

    #         lat,lng = a
    #         m.simple_marker(location = [lat,lng],clustered_marker = True)
    #         #folium.Marker([lat,lng],tooltip='Click for More',popup=country).add_to(m)
    #     except:
    #         continue
    # get html repr of map object
    m = m._repr_html_()
    context = {
        'm':m,
        'form':form,
    }
    return render(request,'index.html',context)
    