from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search
import folium
import geocoder
from .forms import SearchForm
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
    m = folium.Map(location=[27.79,85.2714],zoom_start=6)
    folium.Marker([lat,lng],tooltip='Click for More',popup=country).add_to(m)
    # folium.Marker([27.79,85.2714],tooltip='Click for More',popup="Bagmati").add_to(m)
    
    # get html repr of map object
    m = m._repr_html_()
    context = {
        'm':m,
        'form':form,
    }
    return render(request,'index.html',context)
    