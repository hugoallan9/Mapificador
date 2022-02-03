#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
import math
import uuid

from qgis.utils import iface
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QSize, QPointF, Qt
import os
from pandas import read_excel
import numpy as np
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsApplication,
    QgsGradientColorRamp,
    QgsGraduatedSymbolRenderer,
    QgsCategorizedSymbolRenderer,
    QgsClassificationQuantile,
    QgsMapSettings,
    QgsMapRendererParallelJob,
    QgsFillSymbol,
    QgsPrintLayout,
    QgsLayoutItemMap,
    QgsLayoutPoint,
    QgsUnitTypes,
    QgsLayoutSize,
    QgsLayoutExporter,
    QgsRectangle,
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsPointXY,
    QgsRenderContext,
    QgsLayoutItemPage,
    QgsLegendRenderer,
    QgsLegendStyle,
    QgsRendererCategory,
    QgsSymbol,
    QgsLayout,
 )
from qgis.gui import (
    QgsMapCanvas,
    QgsVertexMarker,
    QgsMapCanvasItem,
    QgsRubberBand,
)


class Mapa:
    def __init__(self):
        self.mapa = None
        self.columnaDeptos = None
        QgsApplication.setPrefixPath("/usr", True)
        self.qgs = QgsApplication([],False)
        self.qgs.initQgis()
        self.proyecto = QgsProject().instance()
        self.colorCyan = QColor(0,174,239,255)
        self.colorBlanco = QColor(255,255,255,255)
        self.paperHeight = 0
        self.paperWidth= 0
        #self.proyecto.removeAllMapLayers()

    def setColor1(self, color):
        self.colorCyan = QColor(color)

    def setColor2(self, color):
        self.colorBlanco = QColor(color)

    def setTamTitulo(self, tam):
        self.tamLetra = tam

    def setTamLeyenda(self, tam):
        self.tamLetraTitulo = tam

    def setTamMapa(self,tam):
        self.tamLetraMapa =tam

    def setTamItem(self,tam):
        self.tamLetraItem = tam

    def setPosxLeyenda(self,pos):
        self.posx = pos

    def setPosyLeyenda(self,pos):
        self.posy = pos

    def getColor1(self):
        return self.colorCyan

    def getColor2(self):
        return self.colorBlanco

    @staticmethod
    def getPaperHeight():
        return 8.5

    @staticmethod
    def getPaperWidth():
        return 11

    @staticmethod
    def getTamLetra():
        return 24

    @staticmethod
    def getTamLetraTitulo():
        return 20

    @staticmethod
    def getTamLetraMapa():
        return 16

    @staticmethod
    def getTamLetraLeyenda():
        return 14

    @staticmethod
    def getTamLetraItem():
        12

    @staticmethod
    def getColorBlanco():
        return QColor(255,255,255,255).name()

    @staticmethod
    def getColorCyan():
        return QColor(0,174,239,255).name()




    def cargar_shape(self, ruta, nombre = "Departamentos"):
        self.mapa = None
        if len(self.proyecto.mapLayers().values()) > 0:
            for layer in self.proyecto.mapLayers().values():
                if layer.name() == nombre:
                    self.mapa = layer
                    break
                else:
                    self.mapa = QgsVectorLayer(ruta, nombre, "ogr")
                    if self.mapa.isValid():
                        self.proyecto.addMapLayer(self.mapa)
                    else:
                        print("Error al cargar el mapa")
        else:
            self.mapa = QgsVectorLayer(ruta, nombre, "ogr")
            if self.mapa.isValid():
                self.proyecto.addMapLayer(self.mapa)
            else:
                print("Error al cargar el mapa")


    @staticmethod
    def cargar_datos(ruta):
        datos = read_excel(ruta, engine='openpyxl')
        #self.datos.dropna(inplace=True)
        datos.fillna(0)
        return datos

    @staticmethod
    def columnasNumericas(datos):
        columnas = datos.select_dtypes(include=np.number).columns.to_list()
        return columnas

    def pintar_mapa_categorias(self, fieldName, color1, color2, mapa):
        rampa = QgsGradientColorRamp(color1,color2,True)
        #Haciendo la categorización de la variable
        fni = mapa.fields().indexFromName(fieldName)
        categorias = mapa.uniqueValues(fni)
        categoriasRender = []
        for cat in categorias:
            symbol = QgsSymbol.defaultSymbol(mapa.geometryType())
            categoriasRender.append(QgsRendererCategory(cat,symbol,str(cat)))
        render_categorizado = QgsCategorizedSymbolRenderer(fieldName, categoriasRender)
        render_categorizado.updateColorRamp(rampa)
        if render_categorizado is not None:
            mapa.setRenderer(render_categorizado)
            mapa.triggerRepaint()

    def get_categories(self, mapa):
        render = mapa.renderer()
        return render.categories()

    def update_labels_categories(self,valores, etiquetas, mapa):
        render = mapa.renderer()
        for cat in render.categories():
            print("Before {}: {} :: {}".format(cat.value(), cat.label(), cat.symbol()))
        for i in range(len(valores)):
            render.updateCategoryLabel(render.categoryIndexForValue(str(valores[i])), str(etiquetas[i]))
        for cat in render.categories():
            print("Update {}: {} :: {}".format(cat.value(), cat.label(), cat.symbol()))


    def pintar_mapa_intervalos(self,fieldName, color1 ,color2, numeroClases):
        '''
                #Crear el método de clasificación
                clasificacion = QgsClassificationQuantile()
                clasificacion.classes(self.mapa, fieldName,4)
                #Creación de render
                clas = clasificacion.classes(self.mapa, fieldName,numeroClases)
                renderer = QgsGraduatedSymbolRenderer(fieldName)
                renderer.setClassAttribute(fieldName)
                renderer.setClassificationMethod(clasificacion)
                renderer.updateColorRamp(rampa)
                #props = {'color_border': 'black', 'style': 'solid', 'style_border': 'solid', 'width_border': '0.4'}
                #symbol = QgsFillSymbol.createSimple(props)
                '''
        rampa = QgsGradientColorRamp(color1,color2,discreto)

        symbol = self.mapa.renderer().symbol()

        renderer = QgsGraduatedSymbolRenderer.createRenderer(self.mapa,
                                                             fieldName, numeroClases, QgsGraduatedSymbolRenderer.Quantile, symbol, rampa)
        self.mapa.setRenderer(renderer)

    def cambiarBorde(self, mapa, color = 'white', grosor = 0.3):
        props = {'color_border': color, 'style': 'solid', 'style_border': 'solid', 'width_border': grosor}
        symbol = QgsFillSymbol.createSimple(props)
        mapa.renderer().updateSymbols(symbol)





    def exportarMapaPruebas(self, mapa):
        image_location = os.path.join('/home/hugog/', "render1.png")
        vlayer = mapa
        settings = QgsMapSettings()
        settings.setLayers([vlayer])
        settings.setBackgroundColor(QColor(255, 255, 255))
        settings.setOutputSize(QSize(800, 600))
        settings.setExtent(vlayer.extent())

        render = QgsMapRendererParallelJob(settings)

        def finished():
            img = render.renderedImage()
            # save the image; e.g. img.save("/Users/myuser/render.png","png")
            img.save(image_location, "png")

        render.finished.connect(finished)

        # Start the rendering
        render.start()

        # The following loop is not normally required, we
        # are using it here because this is a standalone example.
        from qgis.PyQt.QtCore import QEventLoop
        loop = QEventLoop()
        render.finished.connect(loop.quit)
        loop.exec_()

    def cambiarTamHoja(self, layout, size = "Letter", height = 0, width = 0):
        pc = layout.pageCollection()
        if size == "Letter":
            self.paperHeight = 8.5
            self.paperWidth = 11
            self.tamLetra = 24
            self.tamLetraTitulo = 20
            self.tamLetraMapa = 16
            self.tamLetraItem = 14
            self.posx = 8.3
            self.posy = 5.3
        elif size == "Presentation":
            self.paperWidth = 9.40
            self.paperHeight = 9.40 / 2.36
            self.tamLetra = 18
            self.tamLetraTitulo = 16
            self.tamLetraMapa = 14
            self.tamLetraItem = 12
            self.posx = 6
            self.posy = 1.7
        elif size == "Personalizado":
            self.paperHeight = height
            self.paperWidth = width
        pc.pages()[0].setPageSize(QgsLayoutSize(width = self.paperWidth, height = self.paperHeight,
                                                units = QgsUnitTypes.LayoutInches))
        print("Las páginas son:", pc.pages())

    def insertarTitulo(self, layout, titulo):
        label = None
        if layout.itemById('labelTitulo') == None:
            label = QgsLayoutItemLabel(layout)
            label.setId('labelTitulo')
        else:
            label = layout.itemById('labelTitulo')
        label.setText(titulo)
        #math.floor(72 * self.paperHeight * 1 / 10 * 0.5)
        fuente = QFont("Arial", self.tamLetra)
        label.setFont(fuente)
        label.adjustSizeToText()
        tamTexto = label.sizeForText()
        label.attemptMove(
            QgsLayoutPoint(self.paperWidth / 2 - (tamTexto.width() / 2) * 0.0394, 0.01, QgsUnitTypes.LayoutInches))
        layout.addLayoutItem(label)

    def insertarLeyenda(self, posx , posy, layout, titulo = "Leyenda"):
        legend = None
        print("Los items en la página antes de leyenda son", layout.pageCollection().itemsOnPage(0))
        if layout.itemById('leyenda') == None:
            legend = QgsLayoutItemLegend(layout)
            legend.setId('leyenda')
        else:
            print("Se remueve la leyenda")
            legend = layout.itemById('leyenda')


        legend.attemptMove(QgsLayoutPoint(posx, posy,
                                              QgsUnitTypes.LayoutInches))
        legend.setTitle(titulo)
        tree_legend = legend.model().rootGroup()
        for hijo in tree_legend.children():
            print("El nombre del hijo es", hijo.name())
            if hijo.name() == 'result':
                hijo.setName("")
        if len(tree_legend.children()) == 0:
            pass
        print("FINNNNN")
        #tree_legend.children()[0].setName("")
        legend.setStyleFont(QgsLegendStyle.Title, QFont("Arial", self.tamLetraTitulo))
        legend.setStyleFont(QgsLegendStyle.Subgroup, QFont("Arial", self.tamLetraMapa))
        legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont("Arial", self.tamLetraItem))
        layout.addLayoutItem(legend)
        print("Los items en la página despuès de leyenda", layout.pageCollection().itemsOnPage(0))


    def anadirMapaRender(self, layout, mapa, is_there_title = True):
        # Añadiendo mapa
        print("Los items en la página antes del mapa son", layout.pageCollection().itemsOnPage(0))
        mapa_visual = QgsLayoutItemMap(layout)
        if is_there_title:
            mapa_visual.attemptMove(QgsLayoutPoint(self.paperWidth / 20, self.paperHeight * 2 / 20, QgsUnitTypes.LayoutInches))
            mapa_visual.attemptResize(QgsLayoutSize(self.paperHeight * 17 / 20, self.paperWidth, QgsUnitTypes.LayoutInches))
            mapa_visual.setExtent(self.mapa.extent())
        else:
            mapa_visual.attemptMove(QgsLayoutPoint(self.paperWidth/100, self.paperHeight /100, QgsUnitTypes.LayoutInches))
            mapa_visual.attemptResize(QgsLayoutSize(self.paperHeight * 0.94, self.paperWidth , QgsUnitTypes.LayoutInches))
            mapa_visual.setExtent(self.mapa.extent())
        print("El extent es:", mapa.extent())
        layout.addLayoutItem(mapa_visual)
        print("Los items en el layout después de agregar el mapa", layout.items())


    def render(self):
        manager = self.proyecto.layoutManager()
        layoutName = "UNICEF"
        layouts_list = manager.layouts()
        # remove any duplicate layouts
        for lay in layouts_list:
            if lay.name() == layoutName:
                manager.removeLayout(lay)
        layout = QgsPrintLayout(self.proyecto).clone()
        layout.initializeDefaults()
        layout.setName(layoutName)
        manager.addLayout(layout)
        print("Los items en el layout son:", layout.items())
        print("El proyecto asociado es:", layout.project())
        return layout




    def exportarMapa(self, layout, ruta, formato = ""):
        pdfPath = ruta + ".pdf"
        svgPath = ruta + ".svg"
        pngPath = ruta +".png"
        #layout = manager.layoutByName(layoutName)
        exporter = QgsLayoutExporter(layout)
        if formato == "svg":
            exporter.exportToSvg(svgPath, QgsLayoutExporter.SvgExportSettings())
        elif formato == "pdf":
            exporter.exportToPdf(pdfPath,QgsLayoutExporter.PdfExportSettings())
        elif formato == "png":
            exporter.exportToImage(pngPath,QgsLayoutExporter.ImageExportSettings())
        else:
            exporter.exportToSvg(svgPath, QgsLayoutExporter.SvgExportSettings())
            exporter.exportToPdf(pdfPath, QgsLayoutExporter.PdfExportSettings())
            exporter.exportToImage(pngPath, QgsLayoutExporter.ImageExportSettings())
            self.removerLayers()
        #Limpiando el proyecto
        #self.proyecto.clear()
        #self.qgs.exit()


    def removerLayers(self):
        root = self.proyecto.layerTreeRoot()
        for child in root.children():
            print("Estoy presente en el proyecto", child.name())


    def removeLayers(self,layerName):
        for layer in self.proyecto.mapLayers().values():
            if layer.name()==layerName:
                print("Eliminando el layer", layerName)
                QgsProject.instance().removeMapLayers( [layer.id()] )