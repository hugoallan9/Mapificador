from django import forms


class UploadFileForm(forms.Form):
    CHOICES=[('1', 'Departamental'),('2','Municipal')]
    file = forms.FileField()
    tipo_de_mapa = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class escogerVariablesForm(forms.Form):
    def __init__(self, *args, **kargs):
        x , y = None, None
        try:
            x = kargs.pop('x')
            y = kargs.pop('y')
        except:
            pass
        super().__init__(*args, *kargs)
        if x:
            self.fields['codigos']= forms.CharField(
            label='Variable de unión', widget = forms.Select(choices=x))
        if y:
            self.fields['variable_graficar'] = forms.CharField(
            label='Variable a pintar', widget = forms.Select(choices=y))

    tamanios = [
        ('1', 'Carta'),
        ('2', 'Presentacion'),
        ('3', 'Personalizado'),
    ]

    paleta = [
        ('1', 'Continua'),
        ('2', 'Discreta'),
    ]

    codigos = forms.CharField()
    variable_graficar = forms.CharField()
    tipo_paleta = forms.CharField(label='Tipo paleta', widget=forms.Select(choices=paleta))
    tamanio = forms.CharField(label = 'Tamaño del mapa', widget=forms.Select(choices=tamanios))

class parametrosMapaForm(forms.Form):
    titulo = forms.CharField(label= 'Título del mapa', max_length=100, required=False)
    ancho = forms.FloatField(required=True, min_value=1, max_value=50)
    alto = forms.FloatField(required=True, min_value=1, max_value=50)
    color1 = forms.CharField(required=True, label='Color valores bajos', widget=forms.TextInput(attrs={'type': 'color'}))
    color2 = forms.CharField(required=True, label='Color valores altos', widget=forms.TextInput(attrs={'type':'color'}) )
    letraTitulo = forms.IntegerField(required=True, label='Tamaño letra título', min_value=8, max_value=74)
    letraLeyenda = forms.IntegerField(required=True, label='Tamaño letra leyenda',min_value=8, max_value=74)
    letraMapa = forms.IntegerField(required=True, label='Tamaña letra dimensión', min_value=8, max_value=74)
    letraItem = forms.IntegerField(required=True, label='Tamaña letra dimensión', min_value=8, max_value=74)
    tituloLeyenda =  forms.CharField(label= 'Título de leyenda', max_length=100, required=False)
    posxLeyenda = forms.FloatField(required=True, label='Posición x leyenda', min_value=0.01, max_value=50)
    posyLeyenda = forms.FloatField(required=True, label='Posición y leyenda', min_value=0.01, max_value=50)

class parametrosContinuo(parametrosMapaForm):
    numeroClases = forms.FloatField(required=True, label='Número de intervalos', min_value=1, max_value=6)

class parametrosDiscreto(parametrosMapaForm):
    def __init__(self, *args, **kargs):
        numeroCategorias, valores, etiquetas = None, None, None
        try:
            numeroCategorias = kargs.pop('numero_categorias')
            valores = kargs.pop('valores')
            etiquetas = kargs.pop('etiquetas')
        except:
            pass
        super(parametrosDiscreto,self).__init__(*args, **kargs)
        if numeroCategorias:
            for i in range(numeroCategorias):
                self.fields["cat_%d"%i] = forms.CharField(
                    label="Etiqueta para valor {}".format(valores[i]), initial= etiquetas[i] )


