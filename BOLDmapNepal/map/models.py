from xmlrpc.client import NOT_WELLFORMED_ERROR
from django.db import models

# Create your models here.
class Search(models.Model):
     address = models.CharField(max_length=200,null=True)
     date = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
        return self.address

class Listing(models.Model):
   processid = models.CharField(max_length = 60)