from Mapa.MapaDepartamental import MapaDepartamental
from Mapa.MapaMunicipal import MapaMunicipal
from Mapa.mapaClase import Mapa

def mapa_categorias(tipo, ruta_mapa, ruta_excel, variable_union ,variable_pintar, tam_letra_mapa,
                    titulo, tam_letra_titulo, titulo_leyenda, tam_letra_leyenda, posx_leyenda, posy_leyenda,
                    labels_items, tam_letra_item, colores_bajos, colores_altos, ruta_exportacion):
    mapa = None
    if tipo == "1":
        mapa = MapaDepartamental()
    else:
        mapa = MapaMunicipal()
    mapa.cargar_shape(ruta=ruta_mapa)
    mapa_copia = mapa.mapa.clone()
    mapa_copia.setName("Copia")
    mapa.proyecto.addMapLayer(mapa_copia)
    datos = Mapa.cargar_datos(ruta=ruta_excel)
    temp = mapa.crear_layer_datos(datos, x=variable_union, y=variable_pintar)
    mapa.proyecto.addMapLayer(temp)
    mapa.join(mapa_copia, temp, variable_union)
    mapa.setColor1(colores_bajos)
    mapa.setColor2(colores_altos)
    mapa.setTamTitulo(tam_letra_titulo)
    mapa.setTamMapa(tam_letra_mapa)
    mapa.setTamLeyenda(tam_letra_leyenda)
    mapa.setTamItem(tam_letra_item)
    mapa.pintar_mapa_categorias(fieldName='datos_' + variable_pintar,
                             color1=mapa.getColor1(),
                             color2=mapa.getColor2(),
                             mapa=mapa_copia
                             )
    categorias = mapa.get_categories(mapa_copia)
    mapa.update_labels_categories(valores=[cat.value() for cat in categorias],
                                  etiquetas=labels_items, mapa=mapa_copia)
    layout = mapa.render()
    mapa.cambiarTamHoja(layout)
    mapa.anadirMapaRender(layout=layout, mapa=mapa_copia, is_there_title= not (titulo == "") )
    mapa.insertarLeyenda(layout=layout, posx=posx_leyenda, posy=posy_leyenda, titulo= titulo_leyenda)
    mapa.exportarMapa(layout=layout, ruta = ruta_exportacion)
    mapa.removeLayers(temp.name())
    mapa.removeLayers(mapa_copia.name())
    mapa = None
    return categorias
