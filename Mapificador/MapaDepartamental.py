import os.path
from django.conf import settings
from .Mapa import Mapa
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsVectorLayerJoinInfo
from PyQt5.QtCore import QVariant

import os

class MapaDepartamental(Mapa):
    def __init__(self):
        super().__init__()

    def cargar_shape(self, nombre = "Departamentos"):
        self.mapa = QgsVectorLayer(os.path.join(settings.BASE_DIR,'Mapificador',
                                                'departamentos_gtm/departamentos_gtm.shp'), nombre, "ogr")
        if not self.mapa.isValid():
            print("ERROR: El mapa no pudo ser cargado.")
        else:
            self.IdMapa = self.mapa.id()
            self.proyecto.instance().addMapLayer(self.mapa)

    def encontarDeptos(self):
        for column in self.datos:
            if [x for x in range(1,24)] ==  sorted(self.datos[column].values.tolist()):
                self.columnaDeptos = column
                break



    def crear_layer_datos(self, x,y):
        temp = QgsVectorLayer("none","result","memory")
        temp_data = temp.dataProvider()
        #Inicio de la edición
        temp.startEditing()

        #Creación de los campos en el layer temporal
        temp.addAttribute(QgsField(x, QVariant.Double ))
        temp.addAttribute(QgsField(y, QVariant.Double))
        #Actualización de los datos en el layer
        temp.updateFields()

        #Agregando los features
        for row in self.datos.loc[:,[x,y]].itertuples():
            f = QgsFeature()
            f.setAttributes([row[1],row[2]])
            temp.addFeature(f)

        #Empaquetando todo
        temp.commitChanges()
        self.IdDatos = temp.id()
        #Agregar el layer al proyecto
        self.proyecto.instance().addMapLayer(temp)


    def join(self,x):
        info = QgsVectorLayerJoinInfo()
        info.setJoinFieldName(x)
        info.setJoinLayerId(self.IdDatos)
        info.setJoinLayer(self.proyecto.instance().mapLayer(self.IdDatos))
        info.setTargetFieldName("departamen")
        info.setPrefix("datos_")
        self.proyecto.instance().mapLayer(self.IdMapa).addJoin(info)
        self.mapa.updateFields()
        print('Los joins son', self.mapa.vectorJoins())
