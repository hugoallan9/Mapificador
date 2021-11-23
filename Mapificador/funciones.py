from .MapaDepartamental import  MapaDepartamental
from .models import Mapa

def handleUploadedFile(archivo, opcion):
    mapa = Mapa(excel= archivo, tipo_mapa= opcion)
    mapa.save()
    return mapa.id




