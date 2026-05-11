from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.core.validators import RegexValidator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import json
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
                return render(request, 'Html/home.html')

    except ValueError:
        return render(request, 'Html/cadastro.html', dados_preenchidos)
            
    return render(request,"Html/cadastro.html")
    
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
            return render(request, "Html/login.html")
        
    else:
        return render(request, "Html/login.html")
    
def home(request):
    return render(request, "Html/base.html")

def ver_usuario(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
    
    usuarios = {"usuarios" : Usuario.objects.all()}
    
    return render(request, "Html/ver_usuario.html", usuarios)

def editar_usuario(request):
    
    usuario_id = request.user.id
    
    usuario = get_object_or_404(Usuario, id = usuario_id)
    
    if request.method == "POST":
        nome = request.POST.get("nome")
        nomec = request.POST.get("nomec")
        numeroc = request.POST.get("numeroc")
        
        usuario.username = nome
        usuario.nomec = nomec
        usuario.numeroc = numeroc
        usuario.save()

        Log.objects.create(usuario_id = usuario_id, acao = "Edição de perfil")
        return redirect("home")
    
    else: 
        return render(request, "Html/editar_usuario.html")
    
def registro_jogo(request):
    from datetime import datetime
    
    if request.method == "POST":
        data_jogo = request.POST.get("data_hora")

        if not data_jogo:
            return HttpResponse("O campo data de início e final são obrigatórios")

        try:
            data_jogos = datetime.strptime(data_jogo, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("O campo data deve ser uma data válida")

        novo_jogo = Registro(
            data_hora=data_jogos,
        )
        novo_jogo.save()

    registros = Registro.objects.all()

    eventos_json = []

    for registro in registros:

        eventos_json.append({
            "id": registro.id,
            "title": "jogo de volei",
            "start": registro.data_hora.strftime("%Y-%m-%d")
        })

    return render(request, "Html/registros.html", {
        "eventos_json": eventos_json
    })

def deletar_jogo(request, id):
    jogo = Registro.objects.get(id=id)
    jogo.delete()

    return redirect('registro_jogo')

