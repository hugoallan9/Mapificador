#Django imports
import mimetypes
import os.path

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UploadFileForm, escogerVariablesForm, parametrosContinuo, parametrosDiscreto
from django.conf import settings
from .funciones import handleUploadedFile
from Mapa.mapaClase import Mapa
from Mapa.scripts import mapa_categorias

#Model imports
from .models import modeloMapa

# Analisis
import pandas as pd
import random

#Utilities
import uuid
datos = None



def login(request):
    context = {'a':'a'}
    return render(request, 'login.html', context)

def cargaExcel(request):
    context = {}
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            idMapa = handleUploadedFile(request.FILES['file'], form.cleaned_data.get('tipo_de_mapa'))
            return HttpResponseRedirect( str(idMapa)  +  '/paso2')
    else:
        form = UploadFileForm()
        archivoCargado = False
    context['form'] = form
    return render(request, 'paso1.html', context)

def eleccionVariables(request, id):
    pd.set_option('colheader_justify', 'center')
    try:
        datosMapa = modeloMapa.objects.get(pk = id)
    except:
        pass
    datos = Mapa.cargar_datos(ruta=datosMapa.excel.path)
    xLista = Mapa.columnasNumericas(datos)
    yLista = Mapa.columnasNumericas(datos)

    if request.method == "POST":
        x = request.POST['codigos']
        y = request.POST['variable_graficar']
        tamanio = request.POST['tamanio']
        paleta = request.POST['tipo_paleta']
        return HttpResponseRedirect(str(x) +'/'  + str(y) + '/' + str(paleta) + '/' +str(tamanio) + '/paso3')
    else:
        form = escogerVariablesForm(x = [(i,i) for i in xLista], y = [(j,j) for j in yLista])

    context = {
        'excel': datos.to_html(classes='mystyle'),
        'form': form,
    }
    return render(request, 'paso2.html', context)

def graficar(request,id, x, y, paleta, tamanio):
    context = {}
    nombre = ""
    datosMapa = None
    try:
        print("Cargando datos para el mapa")
        datosMapa = modeloMapa.objects.get(pk = id)
    except:
        pass


    if request.method == "POST":
        nombre = str(uuid.uuid4())
        if paleta == '1':
            form = parametrosContinuo(request.POST)
        else:
            form = parametrosDiscreto(request.POST)

        if form.is_valid():
            color1 = form.cleaned_data.get('color1')
            color2 = form.cleaned_data.get('color2')
            titulo = form.cleaned_data.get('titulo')
            letra_mapa = form.cleaned_data.get('letraMapa')
            letra_titulo = form.cleaned_data.get('letraTitulo')
            titulo_leyenda = form.cleaned_data.get('tituloLeyenda')
            letra_leyenda = form.cleaned_data.get('letraLeyenda')
            posx = form.cleaned_data.get('posxLeyenda')
            posy = form.cleaned_data.get('posyLeyenda')
            letra_item = form.cleaned_data.get('letraItem')
            colores_bajos = form.cleaned_data.get('color1')
            colores_altos = form.cleaned_data.get('color2')
            if paleta == '1':
                pass
            elif paleta == '2':
                ruta_mapa = ""
                if datosMapa.tipo_mapa == '1':
                    ruta_mapa = os.path.join(settings.BASE_DIR, 'Mapa', 'departamentos_gtm',
                                             'departamentos_gtm.shp')
                else:
                    ruta_mapa = os.path.join(settings.BASE_DIR, 'Mapa', 'municipios_gtm',
                                             'municipios_gtm.shp')
                datos = Mapa.cargar_datos(datosMapa.excel.path)
                longitud = len(datos[y].unique())
                etiquetas_nuevas = [request.POST.get('cat_%d' % i) for i in range(longitud)]
                ruta = ""
                if datosMapa.tipo_mapa == '1':
                    ruta = os.path.join(settings.BASE_DIR, 'Mapa/departamentos_gtm/departamentos_gtm.shp')
                else:
                    ruta = os.path.join(settings.BASE_DIR, 'Mapa/municipios_gtm/municipios_gtm.shp')
                categorias = mapa_categorias(
                    tipo= datosMapa.tipo_mapa,
                    ruta_mapa = ruta,
                    ruta_excel = datosMapa.excel.path,
                    variable_union = x,
                    variable_pintar = y,
                    tam_letra_mapa = letra_mapa,
                    titulo = titulo,
                    tam_letra_titulo = letra_titulo,
                    titulo_leyenda =titulo_leyenda,
                    tam_letra_leyenda=letra_leyenda,
                    posx_leyenda = posx,
                    posy_leyenda = posy,
                    labels_items = etiquetas_nuevas,
                    tam_letra_item = letra_item,
                    colores_bajos = colores_bajos,
                    colores_altos = colores_altos,
                    ruta_exportacion = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,'Salidas', nombre)
                )
                # updating labels for categorized maps

            if paleta == '1':
                form = parametrosContinuo(request.POST)
            else:
                categorias = categorias
                form = parametrosDiscreto(request.POST,
                                          numero_categorias=len(categorias),
                                          valores =[cat.value() for cat in categorias],
                                          etiquetas=[request.POST.get("cat_%d" %i) for i in range(len(categorias))])
            return render(request, 'paso3.html', {'form':form,
                                                  'tipo_mapa' : paleta,
                                                  'media': settings.MEDIA_ROOT,
                                                  'salida': nombre, })
    else:
        if paleta == '1':
            if tamanio == '1':
                form = parametrosContinuo(initial={'ancho': 11, 'alto':8.5,
                                                   'color1': Mapa.getColorBlanco(),
                                                   'color2': Mapa.getColorCyan(),
                                                   'letraTitulo': Mapa.getTamLetraTitulo(),
                                                   'letraLeyenda': Mapa.getTamLetraLeyenda(),
                                                   'letraMapa': Mapa.getTamLetraMapa(),
                                                   'letraItem': Mapa.getTamLetraItem(),
                                                   'posxLeyenda': 8.3,
                                                   'posyLeyenda': 5.3,
                                                   'numeroClases': 4,
                                                   })
        elif paleta == '2':
            if tamanio == '1':
                datos = Mapa.cargar_datos(datosMapa.excel.path)
                valores = datos[y].unique()
                longitud = len(valores)
                form = parametrosDiscreto(
                numero_categorias=longitud,
                                          valores = valores,
                                          etiquetas=valores,
                    initial={'ancho': 11, 'alto':8.5,
                           'color1': Mapa.getColorBlanco(),
                           'color2': Mapa.getColorCyan(),
                           'letraTitulo': Mapa.getTamLetraTitulo(),
                           'letraLeyenda': Mapa.getTamLetraLeyenda(),
                           'letraMapa': Mapa.getTamLetraMapa(),
                           'letraItem': Mapa.getTamLetraItem(),
                           'posxLeyenda': 8.3,
                           'posyLeyenda': 5.3,
                             },
                )
    context['form'] = form
    context['tipo_mapa'] = paleta
    return render(request, 'paso3.html', context)


def download_file(request, filename=''):
    if filename != '':
        filepath = os.path.join(settings.MEDIA_ROOT, 'Salidas', filename)
        path = open(filepath, 'rb')
        mime_type = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response

