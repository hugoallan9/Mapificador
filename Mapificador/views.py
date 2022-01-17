#Django imports
import os.path

import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, escogerVariablesForm, parametrosContinuo, parametrosDiscreto
from django.conf import settings
from .funciones import handleUploadedFile
from .MapaDepartamental import MapaDepartamental
from .MapaMunicipal import MapaMunicipal
from .Mapa import Mapa

#Model imports
from .models import modeloMapa

# Analisis
import pandas as pd

#Utilities
import time

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
    return render(request, 'index.html', context)

def eleccionVariables(request, id):
    mapa = None
    datosMapa = None
    pd.set_option('colheader_justify', 'center')
    try:
        datosMapa = modeloMapa.objects.get(pk = id)
    except:
        pass
    mapa = Mapa()
    mapa.cargar_datos(ruta=datosMapa.excel.path)
    xLista = mapa.columnasNumericas()
    yLista = mapa.columnasNumericas()




    if request.method == "POST":
        x = request.POST['codigos']
        y = request.POST['variable_graficar']
        tamanio = request.POST['tamanio']
        paleta = request.POST['tipo_paleta']
        return HttpResponseRedirect(str(x) +'/'  + str(y) + '/' + str(paleta) + '/' +str(tamanio) + '/paso3')
    else:
        form = escogerVariablesForm(x = [(i,i) for i in xLista], y = [(j,j) for j in yLista])

    context = {
        'excel': mapa.datos.to_html(classes='mystyle'),
        'form': form,
    }
    mapa.qgs.exit()
    return render(request, 'eleccionVariables.html', context)

def graficar(request,id, x, y, paleta, tamanio):
    context = {}
    nombre = ""
    mapa = None
    try:
        print("Cargando mapa")
        datosMapa = modeloMapa.objects.get(pk = id)
    except:
        pass

    if datosMapa.tipo_mapa ==  '1':
        mapa = MapaDepartamental()
    else:
        mapa = MapaMunicipal()

    mapa.proyecto.clear()
    mapa.cargar_shape()
    mapa.cargar_datos(datosMapa.excel.path)
    mapa.crear_layer_datos(x, y)

    mapa.join(x)




    if request.method == "POST":
        if paleta == '1':
            form = parametrosContinuo(request.POST)
        else:
            form = parametrosDiscreto(request.POST)
        if form.is_valid():
            try:
                print('El número de layers es:', mapa.proyecto.count())
            except:
                print("No hay manager")
            color1 = form.cleaned_data.get('color1')
            color2 = form.cleaned_data.get('color2')
            mapa.setColor1(color1)
            mapa.setColor2(color2)
            mapa.setTamTitulo(form.cleaned_data.get('letraTitulo'))
            mapa.setTamLeyenda(form.cleaned_data.get('letraLeyenda'))
            mapa.setTamMapa(form.cleaned_data.get('letraMapa'))
            mapa.setTamItem(form.cleaned_data.get('letraItem'))
            mapa.setPosxLeyenda(form.cleaned_data.get('posxLeyenda'))
            mapa.setPosyLeyenda(form.cleaned_data.get('posyLeyenda'))
            if paleta == '1':
                mapa.pintar_mapa_intervalos(fieldName='datos_'+y,
                                            color1=mapa.getColor1(),
                                            color2=mapa.getColor2(),
                                            numeroClases=form.cleaned_data.get('numeroClases'))
            elif paleta == '2':
                mapa.pintar_mapa_categorias(fieldName='datos_'+y,
                                            color1=mapa.getColor1(),
                                            color2=mapa.getColor2()
                                            )
                # updating labels for categorized maps

                categorias = mapa.get_categories()
                mapa.update_labels_categories(valores=[cat.value() for cat in categorias],
                                              etiquetas=[
                                                  request.POST.get('cat_%d'%i) for i in range(len(categorias))])
                #mapa.cambiarBorde(color="#808080", grosor=0.4)
            #Creando el render, necesario para tener el layout
            mapa.render()
            #Cambiando tamaño de hoja
            mapa.cambiarTamHoja(mapa.layout, size="Personalizado", height=form.cleaned_data.get('alto'),
                                width=form.cleaned_data.get('ancho'))
            #Cargando el mapa al render
            titulo = form.cleaned_data.get('titulo')
            mapa.anadirMapaRender( titulo != '')

            #Poniendo titulo
            if titulo != '':
                mapa.insertarTitulo(mapa.layout,titulo)
            #Insertando leyenda
            mapa.insertarLeyenda(mapa.layout, form.cleaned_data.get('posxLeyenda'),
                                 form.cleaned_data.get('posyLeyenda'),
                                 titulo=form.cleaned_data.get('tituloLeyenda'))

            #Generación en svg
            nombre = mapa.exportarMapa(ruta=os.path.join(settings.BASE_DIR, "Mapificador","static"))
            if paleta == '1':
                form = parametrosContinuo(request.POST)
            else:
                categorias = mapa.get_categories()
                form = parametrosDiscreto(request.POST,
                                          numero_categorias=len(categorias),
                                          valores =[cat.value() for cat in categorias],
                                          etiquetas=[request.POST.get("cat_%d" %i) for i in range(len(categorias))])
            mapa.qgs.exit()
            return render(request, 'graficar.html', {'form':form, 'salida':os.path.join(nombre + '.svg')})
    else:
        if paleta == '1':
            if tamanio == '1':
                mapa.render()
                mapa.cambiarTamHoja(mapa.layout)
                form = parametrosContinuo(initial={'ancho': 11, 'alto':8.5,
                                                   'color1': mapa.colorBlanco.name(),
                                                   'color2': mapa.colorCyan.name(),
                                                   'letraTitulo': mapa.tamLetra,
                                                   'letraLeyenda': mapa.tamLetraTitulo,
                                                   'letraMapa': mapa.tamLetraMapa,
                                                   'letraItem': mapa.tamLetraItem,
                                                   'posxLeyenda': mapa.posx,
                                                   'posyLeyenda': mapa.posy,
                                                   'numeroClases': 4,
                                                   })
        elif paleta == '2':
            if tamanio == '1':
                mapa.pintar_mapa_categorias(fieldName='datos_'+y,
                                            color1=mapa.getColor1(),
                                            color2=mapa.getColor2()
                                            )
                mapa.render()
                mapa.cambiarTamHoja(mapa.layout)
                categorias = mapa.get_categories()
                form = parametrosDiscreto(
                numero_categorias=len(categorias),
                                          valores =[cat.value() for cat in categorias],
                                          etiquetas=[cat.label() for cat in categorias],
                    initial={'ancho': 11, 'alto': 8.5,
                             'color1': mapa.colorBlanco.name(),
                             'color2': mapa.colorCyan.name(),
                             'letraTitulo': mapa.tamLetra,
                             'letraLeyenda': mapa.tamLetraTitulo,
                             'letraMapa': mapa.tamLetraMapa,
                             'letraItem': mapa.tamLetraItem,
                             'posxLeyenda': mapa.posx,
                             'posyLeyenda': mapa.posy,
                             },
                )

    context['form'] = form
    return render(request, 'graficar.html', context)


