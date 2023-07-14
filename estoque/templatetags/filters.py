from django import template
from estoque.models import Imagem

register = template.Library()

@register.filter(name='get_first_image')
def get_first_image(product):
    # pegando a primeira imagem do produto
    imagem = Imagem.objects.filter(produto=product).first()
    if imagem:
        return imagem.imagem.url # acessa a url da imagem
    else:
        return False