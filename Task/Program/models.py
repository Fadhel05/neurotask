from django.db import models

# Create your models here.
# from django.db.models import BigAutoField
from django.db.models.fields import AutoFieldMixin



class ModelQ(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_address = models.CharField(max_length=100)
    date= models.DateTimeField(auto_now_add=True)
class ModelQQ(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_modelQ = models.ForeignKey(ModelQ,on_delete=models.CASCADE,null=True,blank=True)
    name_address = models.CharField(max_length=100)
    latitude_coordinate_x = models.FloatField()
    longtitude_coordinate_y = models.FloatField()
    distance_to_MKAD= models.CharField(max_length=100)