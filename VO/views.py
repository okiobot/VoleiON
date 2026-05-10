from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.validators import RegexValidator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Função para cadastro dos usuários
def cadastro(request):
    try:
        if request.method == "POST":
            nome = request.POST.get("nome")
            cpf = request.POST.get("cpf")
            data = request.POST.get("data")
            senha = request.POST.get("senha")
            telefone = request.POST.get("telefone")
            funcao = request.POST.get("funcao")
            numeroc = request.POST.get("numeroc")
            nomec = request.POST.get("nomec")
            quantidadec = request.POST.get("quantidadec")
            tamanhoc = request.POST.get("tamanhoc")
            tipoc = request.POST.get("tipoc")
            confirmar_senha = request.POST.get("confirmar_senha")
            
            dados_preenchidos = {'nome_preenchido' : nome,
                            'telefone_preenchido' : telefone,
                            'data_preenchida' : data,
                            'funcao_preenchida' : funcao,
                            'numeroc_preenchido' : numeroc,
                            'nomec_preenchido' : nomec,
                            'quantidadec_preenchida' : quantidadec,
                            'tamanhoc_preenchido' : tamanhoc,
                            'tipoc_preenchida' : tipoc,
                            'cpf_preenchido' : cpf}
        
            validatorE = RegexValidator(regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
            tamanhoT = len(telefone)
            telefone_arrumado = (f"({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}")

            if confirmar_senha != senha:
                print("senhas incorretas")
                return render(request, 'cadastro.html', dados_preenchidos)
        
            if len(cpf) < 11:
                print("O CPF não pode conter menos que 11 dígitos")
                return render(request, 'cadastro.html', dados_preenchidos)
        
            else:
                
                novo_user = Usuario.objects.create(username=nome, cpf=cpf, dataA=data, telefone=telefone, funcao=funcao, numeroc=numeroc, nomec=nomec, 
                                                   quantidadec=quantidadec, tamanhoc=tamanhoc, tipoc=tipoc) 
                novo_user.set_password(senha)
                novo_user.save()        
                return render(request, 'home.html')

    except ValueError:
        return render(request, 'cadastro.html', dados_preenchidos)
            
    return render(request,"cadastro.html")
    
def loginU(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        senha = request.POST.get("senha")
        
        dados_preenchidos = {"nome_preenchido" : nome,
                             "senha_preenchida" : senha}
        
        user = authenticate(request, username=nome, password=senha)            
                
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            print("Nome ou senha incorreto")
            return render(request, "login.html")
        
    else:
        return render(request, "login.html")
    
def home(request):
    return render(request, "home.html")

def ver_usuario(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
    
    usuarios = {"usuarios" : Usuario.objects.all()}
    
    return render(request, "ver_usuario.html", usuarios)

def editar_usuario(request):
    usuario_id = request.user.id
    
    usuario = get_object_or_404(Usuario, id = usuario_id)
    
    if request.method == "POST":
        nome = request.POST.get("nome")
        nomec = request.POST.get("nomec")
        
        usuario.nome = nome
        usuario.nomec = nomec
        usuario.save()

        Registro.objects.create(usuario_id = usuario_id, acao = "Edição de perfil")
        return redirect("home")
    
    else: 
        return render(request, "editar_usuario.html")
    
def registros(request):
    registros = {'registros' : Registro.objects.all().order_by("-data_hora")}
    
    return render(request, "registros.html", registros)