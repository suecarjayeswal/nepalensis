from random import choices
from django import forms
from .models import Search
class SearchForm(forms.ModelForm):
    address = forms.CharField(label='',widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                      'autocomplete': 'off',
                                      'size': '20',
                                      'font-size': 'xx-large',
                                      }),help_text="eg.:species_name=sapiens,")
    class Meta:
        model = Search
        fields = ['address',]
        