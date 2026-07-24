from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.core.validators import RegexValidator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
import json
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from datetime import datetime
from random import * 
import random


# Função para cadastro dos usuários
def cadastro(request):
    try:
        if request.method == "POST":
            nome = request.POST.get("nome")
            cpf = request.POST.get("cpf")
            data_string = request.POST.get("data")
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
                            'data_preenchida' : data_string,
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
        
            data_formatada = datetime.strptime(data_string, "%Y-%m-%d").date()
                
            novo_user = Usuario.objects.create(username=nome, cpf=cpf, data_nasc=data_formatada, telefone=telefone, funcao=funcao, numeroc=numeroc, nomec=nomec, 
                                                quantidadec=quantidadec, tamanhoc=tamanhoc, tipoc=tipoc) 
            novo_user.set_password(senha)
            novo_user.save()        
                
            Log.objects.create(usuario_id=novo_user.id, acao="Cadastro de usuário")
            return render(request, 'Html/login.html')

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
        #numeroc = request.POST.get("numeroc")
        
        usuario.username = nome
        usuario.nomec = nomec
        usuario.save()

        Log.objects.create(usuario_id = usuario_id, acao = "Edição de perfil")
        return redirect("home")
    
    else: 
        return render(request, "Html/editar_usuario.html")
    
def registro_jogo(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        print("erro")
        return redirect("login")
    
    usuario = get_object_or_404(Usuario, id = usuario_id)
    
    if request.method == "POST":
        data_jogo = request.POST.get("data_hora")

        if not data_jogo:
            return HttpResponse("O campo data de início são obrigatórios")

        try:
            data_jogos = datetime.strptime(data_jogo, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("O campo data deve ser uma data válida")

        novo_jogo = Registro(
            nome = "Jogo",
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
            "id": f'jogo_{registro.id}',
            "title" : registro.nome,
            "start": registro.data_hora.strftime("%Y-%m-%d")
        })

    usuarios = Usuario.objects.all()
    
    now = datetime.now()
    ano = now.year

    for u in usuarios:
        if u.data_nasc:
            aniversario = date(ano, u.data_nasc.month, u.data_nasc.day)
        
            eventos_json.append({
                "id" : f"aniversario_{u.id}",
                "title" : f"Aniversário: {u.username}",
                "start" : aniversario.strftime("%Y-%m-%d"),
                "color" : "#D9BB0D",
                "textColor" : "#000000",
                "extendedProps" : {
                    "tipo" : "aniversario"
                }
            })

    return render(request, "Html/registros.html", {
        "eventos_json": eventos_json
        })

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

def iniciar_jogo(request, id):
    usuario_id = request.user.id
    registro = get_object_or_404(Registro, id=id)
    
    if registro.participantes.count() < 1:
        print("O jogo não pode iniciar com menos de 2 jogadores")
        #return redirect('registro_jogo')
        
    registro.status = ("andamento")
    registro.save()
    
    if not Partida.objects.filter(registro=registro).exists():
    
        participantes = list(registro.participantes.all())
        random.shuffle(participantes)
        
        metade = len(participantes) // 2
        
        timeA = participantes[:metade]
        timeB = participantes[metade:]
        
        
        for jogador in timeA:
            Partida.objects.create(
                usuario = jogador,
                registro = registro,
                time = "A"
            )
    
        for jogador in timeB:
            Partida.objects.create(
                usuario = jogador,
                registro = registro,
                time = "B"
            )

    else:
        timeA = [p.usuario for p in Partida.objects.filter(registro=registro, time="A")]
        timeB = [p.usuario for p in Partida.objects.filter(registro=registro, time="B")]

    return render(request, "Html/jogo_live.html", {"jogo" : registro,
                                                 "timeA" : timeA,
                                                 "timeB" : timeB})

def finalizar_jogo(request, id):
    if request.method == "POST":
        print("erro")
        
    registro = get_object_or_404(Registro, id=id)
    
    dados = json.loads(request.body)
    print(dados)
    
    placarA = dados["placarA"]
    placarB = dados["placarB"]
    jogadores = dados["jogadores"]
    
    registro.placarA = placarA
    registro.placarB = placarB
    registro.status = "finalizado"
    
    if placarA > placarB:
        vencedor = "A"
    if placarB > placarA:
        vencedor = "B"
        
    print("Placar A:", placarA)
    print("Placar B:", placarB) 
    print(vencedor)
        
    
    registro.vencedor = vencedor
    registro.save()
    
    for jogador in jogadores:
        partida = Partida.objects.get(
            registro=registro,
            usuario_id=jogador["id"]
        )
        
        print(
        partida.usuario.username,
        partida.time,
        vencedor,
        jogador["pontos"])
        
        partida.pontos = jogador["pontos"]
        partida.venceu = vencedor
        partida.save()
        
    return(JsonResponse({"status" : "ok"}))
    
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

def sair(request):
    if "usuario_id" in request.session:
        del request.session["usuario_id"]
        
    request.session.flush()
        
    return redirect("login")

def perfil(request):
    usuario_id = request.user.id
    
    if not usuario_id:
        redirect("login")
        
    dados = get_object_or_404(Usuario, id=usuario_id)
    
    historico = Partida.objects.filter(usuario=request.user).select_related("registro")
    
    return render(request, "Html/perfil.html", {"usuario" : dados, "historico" : historico})
