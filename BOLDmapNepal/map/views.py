from django.shortcuts import render
import folium
# Create your views here.
def index(request):
    #creating map object
    m = folium.Map(location=[])
    # get html repr of map object
    m = m._repr_html_()
    context = {
        'm':m,
    }
    return render(request,'index.html',context)
    