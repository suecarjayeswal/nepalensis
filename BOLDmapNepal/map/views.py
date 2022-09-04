from django.shortcuts import render
import folium
# Create your views here.
def index(request):
    #creating map object
    m = folium.Map(location=[27.79,85.2714],zoom_start=6)
    folium.Marker([27.79,85.2714],tooltip='Click for More',popup='Bagmati').add_to(m)
    # get html repr of map object
    m = m._repr_html_()
    context = {
        'm':m,
    }
    return render(request,'index.html',context)
    