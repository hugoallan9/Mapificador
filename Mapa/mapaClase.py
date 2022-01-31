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

    def cargar_shape(self, ruta, nombre = "Departamentos"):
        self.mapa = QgsVectorLayer(ruta, nombre, "ogr")
        if not self.mapa.isValid():
            print("ERROR: El mapa no pudo ser cargado.")
        else:
            self.IdMapa = self.mapa.id()
            self.proyecto.instance().addMapLayer(self.mapa)

    def cargar_datos(self, ruta = os.path.join(os.getcwd(),'Datos_pruebas/datos_deptos.xlsx')):
        self.datos = read_excel(ruta, engine='openpyxl')
        #self.datos.dropna(inplace=True)
        self.datos.fillna(0)

    def columnasNumericas(self):
        columnas = self.datos.select_dtypes(include=np.number).columns.to_list()
        return columnas

    def pintar_mapa_categorias(self, fieldName, color1, color2):
        rampa = QgsGradientColorRamp(color1,color2,True)
        #Haciendo la categorización de la variable
        fni = self.mapa.fields().indexFromName(fieldName)
        categorias = self.mapa.uniqueValues(fni)
        categoriasRender = []
        for cat in categorias:
            symbol = QgsSymbol.defaultSymbol(self.mapa.geometryType())
            categoriasRender.append(QgsRendererCategory(cat,symbol,str(cat)))
        render_categorizado = QgsCategorizedSymbolRenderer(fieldName, categoriasRender)
        render_categorizado.updateColorRamp(rampa)
        if render_categorizado is not None:
            self.mapa.setRenderer(render_categorizado)
            self.mapa.triggerRepaint()

    def get_categories(self):
        render = self.mapa.renderer()
        return render.categories()

    def update_labels_categories(self,valores, etiquetas):
        render = self.mapa.renderer()
        for cat in render.categories():
            print("Before {}: {} :: {}".format(cat.value(), cat.label(), cat.symbol()))
        for i in range(len(valores)):
            render.updateCategoryLabel(render.categoryIndexForValue(str(valores[i])), str(etiquetas[i]))
        for cat in render.categories():
            print("Update {}: {} :: {}".format(cat.value(), cat.label(), cat.symbol()))


    def pintar_mapa_intervalos(self,fieldName, color1 ,color2, numeroClases ,discreto = False):
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

    def cambiarBorde(self, color = 'white', grosor = 0.3):
        props = {'color_border': color, 'style': 'solid', 'style_border': 'solid', 'width_border': grosor}
        symbol = QgsFillSymbol.createSimple(props)
        self.mapa.renderer().updateSymbols(symbol)





    def exportarMapaPruebas(self):
        image_location = os.path.join('/home/hugog/', "render1.png")
        vlayer = self.mapa
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
        if self.layout.itemById('labelTitulo') == None:
            label = QgsLayoutItemLabel(layout)
            label.setId('labelTitulo')
        else:
            label = self.layout.itemById('labelTitulo')
        label.setText(titulo)
        #math.floor(72 * self.paperHeight * 1 / 10 * 0.5)
        fuente = QFont("Arial", self.tamLetra)
        label.setFont(fuente)
        label.adjustSizeToText()
        tamTexto = label.sizeForText()
        label.attemptMove(
            QgsLayoutPoint(self.paperWidth / 2 - (tamTexto.width() / 2) * 0.0394, 0.01, QgsUnitTypes.LayoutInches))
        layout.addLayoutItem(label)

    def insertarLeyenda(self, posx , posy,titulo = "Leyenda"):
        legend = None
        print("Los items en la página antes de leyenda son", self.layout.pageCollection().itemsOnPage(0))
        if self.layout.itemById('leyenda') == None:
            legend = QgsLayoutItemLegend(self.layout)
            legend.setLinkedMap(self.mapa_visual)
            legend.setId('leyenda')
        else:
            print("Se remueve la leyenda")
            legend = self.layout.itemById('leyenda')


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
        self.layout.addLayoutItem(legend)
        print("Los items en la página despuès de leyenda", self.layout.pageCollection().itemsOnPage(0))
        print("Los layers cargados son: ", self.proyecto.mapLayers().values())
        layers_names = []
        for layer in self.proyecto.mapLayers().values():
            layers_names.append(layer.name())
            print(layer.id())

        print("layers TOC = {}".format(layers_names))
    def anadirMapaRender(self, is_there_title = True):
        # Añadiendo mapa
        print("Los items en la página antes del mapa son", self.layout.pageCollection().itemsOnPage(0))
        if is_there_title:
            self.mapa_visual = QgsLayoutItemMap(self.layout)
            self.mapa_visual.attemptMove(QgsLayoutPoint(self.paperWidth / 20, self.paperHeight * 2 / 20, QgsUnitTypes.LayoutInches))
            self.mapa_visual.attemptResize(QgsLayoutSize(self.paperHeight * 17 / 20, self.paperWidth, QgsUnitTypes.LayoutInches))
            self.mapa_visual.setExtent(self.mapa.extent())
        else:
            self.mapa_visual = QgsLayoutItemMap(self.layout)
            self.mapa_visual.attemptMove(QgsLayoutPoint(self.paperWidth/100, self.paperHeight /100, QgsUnitTypes.LayoutInches))
            self.mapa_visual.attemptResize(QgsLayoutSize(self.paperHeight * 0.94, self.paperWidth , QgsUnitTypes.LayoutInches))
            self.mapa_visual.setExtent(self.mapa.extent())
        print("El extent es:", self.mapa.extent())
        self.layout.addLayoutItem(self.mapa_visual)
        print("Los items en la página son", self.layout.pageCollection().itemsOnPage(0))
        print("Los items en el layout son:")
        print(self.layout.items())
        for item in self.layout.items():
            if isinstance(item, QgsLayoutItemMap):
                print(item.displayName())


    def render(self):
        self.manager = self.proyecto.layoutManager()
        layoutName = "UNICEF"
        layouts_list = self.manager.layouts()
        # remove any duplicate layouts
        for layout in layouts_list:
            if layout.name() == layoutName:
                self.manager.removeLayout(layout)
        self.layout = QgsPrintLayout(self.proyecto)
        self.layout.initializeDefaults()
        self.layout.setName(layoutName)
        self.manager.addLayout(self.layout)
        print("El proyecto asociado es:", self.layout.project())




    def exportarMapa(self, ruta, formato = ""):
        pdfPath = ruta + ".pdf"
        svgPath = ruta + ".svg"
        pngPath = ruta +".png"
        #layout = manager.layoutByName(layoutName)
        exporter = QgsLayoutExporter(self.layout)
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
        """
        root = self.proyecto.layerTreeRoot()
        root.removeLayer(self.mapa)
        root.removeLayer(self.temp)
        """
        root = self.proyecto.layerTreeRoot()
        for child in root.children():
            print("Estoy presente en el proyecto", child.name())
