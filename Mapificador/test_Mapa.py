from unittest import TestCase
from Mapa.MapaDepartamental import  MapaDepartamental

import os
class TestMapa(TestCase):
    def setUp(self) -> None:
        self.mapa = MapaDepartamental()

    def test_pintar_mapa_categorias(self):
        self.mapa = MapaDepartamental()
        self.mapa.cargar_shape()
        self.mapa.cargar_datos(ruta=os.path.join('/home/hugo/PycharmProjects/Mapificador/' ,'uploads', 'datos_deptos.xlsx'))
        self.mapa.pintar_mapa_categorias('Salud', self.mapa.getColor1(), self.mapa.getColor2())
