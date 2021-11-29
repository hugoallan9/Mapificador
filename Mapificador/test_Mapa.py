from unittest import TestCase
from Mapa import Mapa
from MapaDepartamental import  MapaDepartamental
from django.conf import settings
import os
class TestMapa(TestCase):
    def setUp(self) -> None:
        self.mapa = MapaDepartamental()

    def test_pintar_mapa_categorias(self):
        self.mapa.cargar_datos(ruta=os.path.join(settings.BASE_DIR,'uploads', 'datos_deptos.xlsx'))
        self.mapa.pintar_mapa_categorias('Salud', self.mapa.getColor1(), self.mapa.getColor2())
