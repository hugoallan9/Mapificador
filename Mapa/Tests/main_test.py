from Mapa.MapaDepartamental import MapaDepartamental





def main():
    mapa1 = MapaDepartamental()
    mapa1.proyecto.clear()
    mapa1.cargar_shape(ruta = '/home/hugog/GitHub/Mapas/Mapa/departamentos_gtm/departamentos_gtm.shp')
    mapa1.cargar_datos(ruta='/home/hugog/GitHub/Mapas/uploads/datos_deptos.xlsx')
    mapa1.crear_layer_datos(x = "Código Departamento", y = "Educación")
    mapa1.join('Código Departamento')
    mapa1.setColor1("#FFFFFF")
    mapa1.setColor2("#00FFFF")
    mapa1.pintar_mapa_categorias(fieldName='datos_' + 'Educación',
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
    mapa1.proyecto.clear()
    mapa1 = None
    print("-----------------------------------------------------")
    mapa2 = MapaDepartamental()
    mapa2.proyecto.clear()
    mapa2.cargar_shape(ruta = '/home/hugog/GitHub/Mapas/Mapa/departamentos_gtm/departamentos_gtm.shp')
    mapa2.cargar_datos(ruta='/home/hugog/GitHub/Mapas/uploads/datos_deptos.xlsx')
    mapa2.crear_layer_datos(x = "Código Departamento", y = "Wash")
    mapa2.join('Código Departamento')
    mapa2.setColor1("#FFFFFF")
    mapa2.setColor2("#00FFFF")
    mapa2.pintar_mapa_categorias(fieldName='datos_' + 'Wash',
                                color1=mapa2.getColor1(),
                                color2=mapa2.getColor2()
                                )
    mapa2.render()
    mapa2.cambiarTamHoja(mapa2.layout)
    mapa2.anadirMapaRender(False)
    mapa2.insertarLeyenda(posx=8.3, posy=5.3)
    mapa2.exportarMapa('/home/hugog/prueba2', formato="pdf")
    mapa2.exportarMapa('/home/hugog/prueba2', formato="svg")
    mapa2.proyecto.removeAllMapLayers()
    #mapa1.qgs.exitQgis()

main()
