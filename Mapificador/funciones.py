from .MapaDepartamental import  MapaDepartamental
from .models import modeloMapa

def handleUploadedFile(archivo, opcion):
    mapa = modeloMapa(excel= archivo, tipo_mapa= opcion)
    mapa.save()
    return mapa.id




