import django_filters
from .models import *

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = Listing
        #fields = '__all__'
        fields = {
            'processid':['exact'],
        }
        
