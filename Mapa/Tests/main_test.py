from Mapa.MapaDepartamental import MapaDepartamental
from Mapa.mapaClase import Mapa
import random




def main(variables):
    y = random.choices(variables)[0]
    mapa1 = MapaDepartamental()
    mapa1.cargar_shape(
        ruta = '/home/hugog/GitHub/Mapas/Mapa/departamentos_gtm/departamentos_gtm.shp')
    mapa = mapa1.mapa.clone()
    mapa.setName("Copia")
    mapa1.proyecto.addMapLayer(mapa)
    datos = Mapa.cargar_datos(ruta='/home/hugog/GitHub/Mapas/uploads/datos_deptos.xlsx')
    temp = mapa1.crear_layer_datos(datos, x = "Código Departamento", y = y)
    mapa1.proyecto.addMapLayer(temp)
    mapa1.join(mapa, temp,'Código Departamento')
    mapa1.setColor1("#FFFFFF")
    mapa1.setColor2("#00FFFF")
    mapa1.pintar_mapa_categorias(fieldName='datos_' + y,
                                color1=mapa1.getColor1(),
                                color2=mapa1.getColor2(),
                                mapa=mapa
                                )
    layout = mapa1.render()
    mapa1.cambiarTamHoja(layout)
    mapa1.anadirMapaRender(layout=layout, mapa = mapa, is_there_title=False)
    mapa1.insertarLeyenda(layout=layout, posx=8.3, posy=5.3)
    mapa1.exportarMapa(layout=layout, ruta = '/home/hugog/pruebaNueva' + y , formato="pdf")
    mapa1.exportarMapa(layout=layout, ruta = '/home/hugog/pruebaNueva' + y, formato="svg")
    mapa1.exportarMapa(layout=layout, ruta = '/home/hugog/pruebaNueva' + y, formato="png")
    mapa1.proyecto.write('/home/hugog/prueba_manual.qgs')
    mapa1.removeLayers(temp.name())
    mapa1.removeLayers(mapa.name())
    #mapa1 = None

