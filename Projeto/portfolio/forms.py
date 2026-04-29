from django import forms
from .models import *

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'data', 'imagem', 'video_demo', 'conceitos_aplicados', 'utilizador', 'uc', 'tecnologias', 'competencias']

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = ['nome', 'tipo', 'descricao', 'logo', 'website_url', 'nivel_preferencia']

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = ['nome', 'tipo', 'nivel', 'descricao']

class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = ['titulo', 'instituicao', 'data_inicio', 'data_fim', 'certificado_url', 'descricao', 'competencias']