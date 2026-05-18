from django import forms
from .models import Artigo, Comentario, Avaliacao


class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']


class ComentarioForm(forms.ModelForm):
    nome_autor = forms.CharField(
        max_length=100,
        required=False,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'O teu nome (opcional)'}),
    )

    class Meta:
        model = Comentario
        fields = ['nome_autor', 'texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreve o teu comentário...'}),
        }


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['pontuacao']
        widgets = {
            'pontuacao': forms.RadioSelect(choices=Avaliacao.PONTUACOES),
        }
        labels = {'pontuacao': 'A tua pontuação'}
