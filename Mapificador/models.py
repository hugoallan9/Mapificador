from django.db import models
import os
# Create your models here.

class Mapa(models.Model):
    TIPO_MAPA = (
        ('1', 'Departamental' ),
        ('2', 'Municipal'),
    )
    id = models.AutoField(primary_key=True)
    excel = models.FileField(upload_to='uploads/')
    tipo_mapa = models.CharField(max_length=1,choices=TIPO_MAPA)
