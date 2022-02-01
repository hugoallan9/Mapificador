from Mapa.MapaDepartamental import MapaDepartamental
from Mapa.mapaClase import Mapa
from Mapificador import config
import threading


class hiloMapa(threading.Thread):

    def __init__(self, y):
        self.y = y
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("Ejecución iniciada")
            print("Variable a pintar", self.y)
            mapa1 = MapaDepartamental()
            for layer in mapa1.proyecto.mapLayers().values():
                print("Nombres antes de cargar todo:", layer.name())
            mapa1.cargar_shape(
                ruta='/home/hugog/GitHub/Mapas/Mapa/departamentos_gtm/departamentos_gtm.shp')
            mapa = mapa1.mapa.clone()
            mapa.setName("Copia")
            mapa1.proyecto.addMapLayer(mapa)
            datos = Mapa.cargar_datos(ruta='/home/hugog/GitHub/Mapas/uploads/datos_deptos.xlsx')
            temp = mapa1.crear_layer_datos(datos, x="Código Departamento", y=self.y)
            mapa1.proyecto.addMapLayer(temp)
            mapa1.join(mapa, temp, 'Código Departamento')
            mapa1.setColor1("#FFFFFF")
            mapa1.setColor2("#00FFFF")
            mapa1.pintar_mapa_categorias(fieldName='datos_' + self.y,
                                         color1=mapa1.getColor1(),
                                         color2=mapa1.getColor2(),
                                         mapa=mapa
                                         )
            mapa1.proyecto.write("/home/hugog/prueba.qgs")
            layout = mapa1.render()
            mapa1.cambiarTamHoja(layout)
            mapa1.anadirMapaRender(layout=layout, mapa=mapa, is_there_title=False)
            mapa1.insertarLeyenda(layout=layout, posx=8.3, posy=5.3)
            mapa1.exportarMapa(layout=layout, ruta='/home/hugog/pruebaNueva' + self.y, formato="pdf")
            mapa1.exportarMapa(layout=layout, ruta='/home/hugog/pruebaNueva'+ self.y, formato="svg")
            #mapa1.exportarMapa(layout=layout, ruta='/home/hugog/pruebaNueva'+ self.y, formato="png")
            mapa1.exportarMapaPruebas(mapa = mapa)
            mapa1.removeLayers(temp.name())
            mapa1.removeLayers(mapa.name())
            mapa1.removerLayers()
            mapa1.proyecto.write('/home/hugog/prueba_manual.qgs')
            for layer in mapa1.proyecto.mapLayers().values():
                print("Nombres:", layer.name())
            mapa1 = None
            print("-----------------------------------------------------")
            mapa1 = MapaDepartamental()
            mapa1.cargar_shape(
                ruta='/home/hugog/GitHub/Mapas/Mapa/departamentos_gtm/departamentos_gtm.shp')
            mapa = mapa1.mapa.clone()
            mapa1.proyecto.addMapLayer(mapa)
            datos = Mapa.cargar_datos(ruta='/home/hugog/GitHub/Mapas/uploads/datos_deptos.xlsx')
            temp = mapa1.crear_layer_datos(datos, x="Código Departamento", y="Wash")
            mapa1.proyecto.addMapLayer(temp)
            mapa1.join(mapa, temp, 'Código Departamento')
            mapa1.setColor1("#FFFFFF")
            mapa1.setColor2("#00FFFF")
            mapa1.pintar_mapa_categorias(fieldName='datos_' + 'Wash',
                                         color1=mapa1.getColor1(),
                                         color2=mapa1.getColor2(),
                                         mapa=mapa
                                         )
            layout = mapa1.render()
            mapa1.cambiarTamHoja(layout)
            mapa1.anadirMapaRender(layout=layout, mapa=mapa, is_there_title=False)
            mapa1.insertarLeyenda(layout=layout, posx=8.3, posy=5.3)
            mapa1.exportarMapa(layout=layout, ruta='/home/hugog/pruebaNueva2', formato="pdf")
            mapa1.exportarMapa(layout=layout, ruta='/home/hugog/pruebaNueva2', formato="svg")
            mapa1.exportarMapa(layout=layout, ruta='/home/hugog/pruebaNueva2', formato="png")
            mapa1.proyecto.write('/home/hugog/prueba_manual.qgs')
            mapa1.proyecto.removeAllMapLayers()
            mapa1.proyecto.clear()
            mapa1 = None
        except Exception as e:
            print("Ocurrió un error",e)







