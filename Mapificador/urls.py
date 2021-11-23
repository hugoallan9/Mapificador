from django.urls import path
from .views import cargaExcel, eleccionVariables, graficar
urlpatterns = [
    path('cargarExcel', cargaExcel, name='carga' ),
    path('<str:id>/paso2', eleccionVariables, name='variables'),
    path('<str:id>/<str:x>/<str:y>/<str:paleta>/<str:tamanio>/paso3', graficar, name = 'graficar')
    ]