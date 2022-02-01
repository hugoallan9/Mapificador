import os.path
from django.conf import settings
from .mapaClase import Mapa
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsVectorLayerJoinInfo
from PyQt5.QtCore import QVariant

import os

class MapaDepartamental(Mapa):
    def __init__(self):
        super().__init__()



    def encontarDeptos(self):
        for column in self.datos:
            if [x for x in range(1,24)] ==  sorted(self.datos[column].values.tolist()):
                self.columnaDeptos = column
                break

    def crear_layer_datos2(self,datos,x,y):
        uri = 'file:///home/hugog/datos_deptos.csv?delimiter=,'
        csvLayer = QgsVectorLayer(uri,"result", "delimitedText")
        return csvLayer


    def crear_layer_datos(self, datos, x,y):
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
        for row in datos.loc[:,[x,y]].itertuples():
            f = QgsFeature()
            f.setAttributes([row[1],row[2]])
            temp.addFeature(f)

        #Empaquetando todo
        temp.commitChanges()
        IdDatos = temp.id()
        for feature in temp.getFeatures():
            print(feature[0],feature[1])
        #Agregar el layer al proyecto
        return temp


    def join(self,mapa, datos, x):
        for field in mapa.fields():
            print(field.name())
        info = QgsVectorLayerJoinInfo()
        info.setJoinFieldName(x)
        info.setJoinLayerId(datos.id())
        info.setJoinLayer(self.proyecto.mapLayer(datos.id()))
        info.setTargetFieldName("departamen")
        info.setPrefix("datos_")
        self.proyecto.mapLayer(mapa.id()).addJoin(info)
        self.mapa.updateFields()
        print('Los joins son', mapa.vectorJoins())
        for field in mapa.fields():
            print(field.name())
