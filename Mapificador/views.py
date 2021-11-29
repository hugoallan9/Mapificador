#Django imports
import os.path

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, escogerVariablesForm, parametrosContinuo
from django.conf import settings
from .funciones import handleUploadedFile
from .MapaDepartamental import MapaDepartamental

#Model imports
from .models import Mapa

# Analisis
import pandas as pd



datos = None



def indexPage(request):
    context = {'a':'a'}
    return render(request, 'home.html', context)

def cargaExcel(request):
    context = {}
    mapa = None
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            idMapa = handleUploadedFile(request.FILES['file'], form.cleaned_data.get('tipo_de_mapa'))
            return HttpResponseRedirect( str(idMapa)  +  '/paso2')
    else:
        form = UploadFileForm()
        archivoCargado = False
    context['form'] = form
    return render(request, 'cargaExcel.html', context)

def eleccionVariables(request, id):
    mapa = None
    pd.set_option('colheader_justify', 'center')
    try:
        datosMapa = Mapa.objects.get(pk = id)
    except:
        pass
    if datosMapa.tipo_mapa ==  '1':
        mapa = MapaDepartamental()
        mapa.cargar_datos(datosMapa.excel.path)
        mapa.encontarDeptos()
        xLista = [mapa.columnaDeptos]
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
    return render(request, 'eleccionVariables.html', context)

def graficar(request,id, x, y, paleta, tamanio):
    context = {}
    nombre = ""
    mapa = None
    try:
        print("Cargando mapa")
        datosMapa = Mapa.objects.get(pk = id)
    except:
        pass

    if datosMapa.tipo_mapa ==  '1':
        mapa = MapaDepartamental()
        mapa.proyecto.clear()
        mapa.cargar_shape()
        mapa.cargar_datos(datosMapa.excel.path)
        mapa.crear_layer_datos(x,y)

    mapa.join(x)




    if request.method == "POST":
        form = parametrosContinuo(request.POST)
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
            return render(request, 'graficar.html', {'form':form, 'salida':os.path.join(nombre + '.svg')})
    else:
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

    context['form'] = form
    return render(request, 'graficar.html', context)


