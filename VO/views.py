from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.core.validators import RegexValidator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import json
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

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
        
            #validatorE = RegexValidator(regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
            #tamanhoT = len(telefone)
            #telefone_arrumado = (f"({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}")

            if confirmar_senha != senha:
                print("senhas incorretas")
                return render(request, 'Html/cadastro.html', dados_preenchidos)
        
            if len(cpf) < 11:
                print("O CPF não pode conter menos que 11 dígitos")
                return render(request, 'Html/cadastro.html', dados_preenchidos)
        
            else:
                
                novo_user = Usuario.objects.create_user(username=nome, cpf=cpf, dataA=data, telefone=telefone, funcao=funcao, numeroc=numeroc, nomec=nomec, 
                                                   quantidadec=quantidadec, tamanhoc=tamanhoc, tipoc=tipoc) 
                novo_user.set_password(senha)
                novo_user.save()        
                return render(request, 'Html/base.html')

    except ValueError:
        return render(request, 'Html/cadastro.html', dados_preenchidos)
            
    return render(request,"Html/cadastro.html")
    
def loginU(request):
    if request.method == "POST":
        cpf = request.POST.get("cpf")
        senha = request.POST.get("senha")
        
        dados_preenchidos = {"cpf_preenchido" : cpf,
                             "senha_preenchida" : senha}
        
        user = authenticate(request, username=cpf, password=senha)            
                
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            print("Nome ou senha incorreto")
            return render(request, "Html/login.html")
        
    else:
        return render(request, "Html/login.html")
    
def home(request):
    registros = Registro.objects.all()

    eventos_json = []

    for registro in registros:

        eventos_json.append({
            "id": registro.id,
            "title": f"Jogo {registro.id}",
            "start": registro.data_hora.strftime("%Y-%m-%d")
        })

    return render(request, "Html/base.html", {
        "eventos_json": eventos_json
    })

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
        #numeroc = request.POST.get("numeroc")
        
        usuario.username = nome
        usuario.nomec = nomec
        usuario.save()

        Log.objects.create(usuario_id = usuario_id, acao = "Edição de perfil")
        return redirect("home")
    
    else: 
        return render(request, "Html/editar_usuario.html")
    
def registro_jogo(request):
    from datetime import datetime
    
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
    
    usuario = get_object_or_404(Usuario, id = usuario_id)
    
    if request.method == "POST":
        data_jogo = request.POST.get("data_hora")

        if not data_jogo:
            return HttpResponse("O campo data de início é obrigatório")

        try:
            data_jogos = datetime.strptime(data_jogo, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("O campo data deve ser uma data válida")

        novo_jogo = Registro(
            data_hora=data_jogos,
            criador= usuario
        )
        
        novo_jogo.save()
        
        novo_jogo.participantes.add(usuario)
        
        Log.objects.create(usuario_id=usuario_id, jogo=novo_jogo.id, acao="Criação de jogo")

        return JsonResponse({
            "id": novo_jogo.id
        })

    registros = Registro.objects.all()

    eventos_json = []

    for registro in registros:

        eventos_json.append({
            "id": registro.id,
            "title" : f"Jogo {registro.id}",
            "start": registro.data_hora.strftime("%Y-%m-%d")
        })
    print(eventos_json)
    return render(request, "Html/registros.html", {"eventos_json": eventos_json})

from django.http import JsonResponse

def detalhe_jogo(request, id):
    jogo = get_object_or_404(Registro, id=id)
    usuario_atual = request.user
    
    lista_participantes = [u.username for u in jogo.participantes.all()]
    
    ja_inscrito = jogo.participantes.filter(id=usuario_atual.id).exists()
    
    criador = (jogo.criador == usuario_atual)
    
    dados = {
        "id": jogo.id,
        "nome": jogo.nome,
        "data_hora": jogo.data_hora.strftime("%d/%m/%Y"), 
        "organizador": jogo.criador.username,
        "quant_participantes": jogo.participantes.count(),
        "participantes" : lista_participantes,
        "ja_inscrito" : ja_inscrito,
        "criador" : criador}
    
    return JsonResponse(dados)

def inscrever_jogo(request, id):
    if request.method == "POST":
        jogo = get_object_or_404(Registro, id=id)
        jogo.participantes.add(request.user)
        return JsonResponse({"sucesso" : True, "mensagem" : "Inscrição realizada"})
    return JsonResponse({"sucesso" : False}, status = 400)

def sair_jogo(request, id):
    if request.method == "POST":
        jogo = get_object_or_404(Registro, id=id)
        jogo.participantes.remove(request.user)
        return JsonResponse({"sucesso" : True, "mensagem" : "Saída realizada"})
    return JsonResponse({"sucesso" : False}, status = 400)
    
def deletar_jogo(request, id):
    usuario_id = request.user.id
    jogo = Registro.objects.get(id=id)

    Log.objects.create(usuario_id=usuario_id, jogo=jogo.id, acao="Exclusão de jogo")
    
    jogo.delete()

    return redirect('registro_jogo')

def jogos_disponiveis(request):
    pass

def logout(request):
    if "usuario_id" in request.session:
            del request.session["usuario_id"]
            
    request.session.flush()
            
    return redirect("login")


    
    
#recebe um usuario e retorna True se a data de nascimento for igual a data atual
def aniversariante_Check(usuario):

    data_atual = date.today()

    if usuario.data_nasc.day == data_atual.day and usuario.data_nasc.month == data_atual.month:
        return True
    return False

#retorna retorna todos os aniversariantes do dia no BD
def aniversariante_dia(request, id):
   
   usuario = get_object_or_404(Usuario, id = usuario_id)
   
   data_atual = date.today()
   
   aniversariantes_dia = Usuario.objects.filter(data_nasc__day=data_atual.day, data_nasc__month=data_atual.month).only('username', 'data_nasc')
   
   return render(request, "Html/aniversariantes_dia.html", {"aniversariantes_dia": aniversariantes_dia})
    
def tesouraria(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
      
    if request.method == "POST":
        cancelar_id = request.POST.get("cancelar")

        if cancelar_id:
            Usuario.objects.filter(id=cancelar_id).update(pagamento="Pendente")
            Log.objects.create(usuario_id=usuario_id, acao="Cancelamento de pagamento")
            
        else:
            pagos = request.POST.getlist("usuarios_pagos")
            if pagos:
                Usuario.objects.filter(id__in=pagos).update(pagamento="Pago")
                Log.objects.create(usuario_id=usuario_id, acao="Confirmação de pagamento")
        
        return redirect("tesouraria")
    
    return render(request, "Html/tesouraria.html", {"usuarios" : Usuario.objects.all()})

#retorna todos os aniversariantes do mes no BD
def aniversariante_mes(request, id):
    usuario = get_object_or_404(Usuario, id = usuario_id)
    
    data_atual = date.today()
    
    aniversariantes_mes = Usuario.objects.filter(data_nasc__month=data_atual.month).only('username', 'data_nasc')
    
    #Não sei o url coerreto para essa função, deixei essa como placeholder
    return render(request, "Html/aniversariantes_mes.html", {"aniversariantes_mes": aniversariantes_mes})
  
def deletar_usuario(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
    
    senha = request.POST.get("senha")
        
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, id = usuario_id)
    
        if not check_password(senha, usuario.password):
            print("Senha incorreta")
            return render(request, "Html/deletar_usuario.html")
        
        else:
            print("Perfil deletado")
            Log.objects.create(usuario=usuario_id, acao="Exclusão de usuário")
            usuario.delete()
            return redirect("login")
    
    return render(request, "Html/deletar_usuario.html")
        
def logs(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
    
    return render(request, "Html/logs.html", {"registros" : Log.objects.all()})

def get_aniver_all(request):
    aniversariantes = Usuario.objects.annotate(
        dia_aniversario=models.functions.ExtractDay('data_nasc'),
        mes_aniversario=models.functions.ExtractMonth('data_nasc')
    ).order_by('mes_aniversario', 'dia_aniversario').only('username', 'data_nasc')
    #Não sei o url coerreto para essa função, deixei essa como placeholde
    return render(request, "Html/aniversariantes_all.html", {"aniversariantes": aniversariantes})


