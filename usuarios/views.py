from django.shortcuts import render, HttpResponse
from rolepermissions.decorators import has_permission_decorator
from . models import Users
from django.shortcuts import redirect #redireciona a pagina
from django.urls import reverse # reverte o caminho da pagina para a name da urls
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib import messages

@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == 'GET':
        vendedores = Users.objects.filter(cargo="V")
        return render(request, 'cadastrar_vendedor.html', {'vendedores': vendedores})
    if request.method == 'POST':
        email = request.POST.get('email') #captura o que foi digitado no input da página
        senha = request.POST.get('senha')

        user = Users.objects.filter(email=email)

        if user.exists(): # se existe algum dado nessa variavel
            # TODO: utilizar messages do django
            return HttpResponse('Email já existe')
        
        #cria o usuario e atribui o username ao email, para fazer autenticação pelo username 
        user = Users.objects.create_user(username=email, email=email, password=senha, cargo='V') 

        # TODO: Redirecionar com uma mensagem
        return HttpResponse('Conta criada com sucesso')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('plataforma')) 
        return render(request, 'login.html')
    elif request.method == 'POST':
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        #se o usuário não existir
        if not user:
            # TODO: Redirecionar com mensagem de erro
            return HttpResponse('Usuário inválido')

        #se o usuario existir fazer o login
        auth.login(request, user)
        return HttpResponse('Usuário logado com sucesso')

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))

@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id): # esse é o id passado na url
    vendedor = get_object_or_404(Users, id=id) # tabela que vai procurar Users e bucar o ususario pelo id que é igual ao id da url
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS, 'Vendedor excluído com sucesso.')
    return redirect(reverse('cadastrar_vendedor'))