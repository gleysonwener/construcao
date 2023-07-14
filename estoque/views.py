from django.shortcuts import render
from .models import Categoria, Produto, Imagem
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator
from .forms import ProdutoForm

@has_permission_decorator('cadastrar_produtos')
def add_produto(request):
    if request.method == "GET":
        categorias = Categoria.objects.all() #captura todas as categorias
        produtos = Produto.objects.all() # captura todos os produtos
        # reinderizando no html
        return render(request, 'add_produto.html', {'categorias': categorias, 'produtos': produtos}) # context de categorias e produtos
    elif request.method == "POST":
        #pegando todos os dados digitados pelo usuario
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        preco_compra = request.POST.get('preco_compra')
        preco_venda = request.POST.get('preco_venda')
        #imagens = request.FILES.getlist('imagens')

        #salvar produto no banco
        produto = Produto(nome=nome, categoria_id=categoria, quantidade=quantidade, 
                          preco_compra=preco_compra, preco_venda=preco_venda)
        produto.save()
        
        #iterando a lista de imagens
        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg' # output - como vai ficar a saida

            img = Image.open(f)   #  abrindo a imagem
            img = img.convert('RGB')  #  convertendo a imagem para RGB
            img = img.resize((300,300))  # redefinindo o tamanho da imagem em x,y
            draw = ImageDraw.Draw(img) # desenhar a imagem - imagem na variavel img
            # desenha na imagem - posição x,y - texto com data e cor em RGB
            draw.text((20,280), f'CONSTRUCT {date.today()}', (255,255,255))       
            #permite chamar a variável ao invés de um caminho na hora de salvar ou no save e aceita bytes
            output = BytesIO()
            # pegando a imagem e salvando em bytes
            img.save(output, format='JPEG', quality=100) 
            # voltando o ponteiro para o inicio - endereçamento da memoria
            output.seek(0)
            #finalizando a imagem
            img_final = InMemoryUploadedFile(output, 'ImageField', name, 'image/jpeg', sys.getsizeof(output), None)

            img_dj = Imagem(imagem = img_final, produto=produto)
            img_dj.save()
        #adcionando messages
        messages.add_message(request, messages.SUCCESS, 'Produto cadastrado comsucesso.')
        # reverse espera o name da url
        return redirect(reverse('add_produto'))

def produto(request, slug):
    if request.method == 'GET':
        produto = Produto.objects.get(slug=slug)
        #print(produto.__dict__)
        #form = ProdutoForm(initial={'nome': produto.nome})
        data = produto.__dict__
        data['categoria'] = produto.categoria.id # cria a posição data de categoria para mostrar no formulário
        form = ProdutoForm(initial=data)
        return render(request, 'produto.html', {'form' : form})