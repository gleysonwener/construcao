from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta(): # classe de configuração
        model = Produto
        fields = "__all__"
        