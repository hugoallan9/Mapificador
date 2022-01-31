from Mapa.MapaDepartamental import MapaDepartamental

import threading


class hiloMapa(threading.Thread):

    def __init__(self, y):
        self.y = y
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("Ejecución iniciada")
            mapa1 = MapaDepartamental()
            mapa1.constructor()
            mapa1.cargar_shape(ruta='/home/hugog/GitHub/Mapas/Mapa/departamentos_gtm/departamentos_gtm.shp')
            mapa1.cargar_datos(ruta='/home/hugog/GitHub/Mapas/uploads/datos_deptos.xlsx')
            mapa1.crear_layer_datos(x="Código Departamento", y=self.y)
            mapa1.join('Código Departamento')
            mapa1.setColor1("#FFFFFF")
            mapa1.setColor2("#00FFFF")
            mapa1.pintar_mapa_categorias(fieldName='datos_' + self.y,
                                         color1=mapa1.getColor1(),
                                         color2=mapa1.getColor2()
                                         )
            mapa1.render()
            mapa1.cambiarTamHoja(mapa1.layout)
            mapa1.anadirMapaRender(False)
            mapa1.insertarLeyenda(posx=8.3, posy=5.3)
            mapa1.exportarMapa('/home/hugog/prueba', formato="pdf")
            mapa1.exportarMapa('/home/hugog/prueba', formato="svg")
            mapa1.exportarMapa('/home/hugog/prueba', formato="png")
            mapa1.proyecto.write('/home/hugog/prueba_manual.qgs')
            mapa1.proyecto.removeAllMapLayers()
            mapa1 = None
            print("-----------------------------------------------------")

        except Exception as e:
            print(e)







