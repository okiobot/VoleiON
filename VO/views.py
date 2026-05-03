from django.shortcuts import render, redirect
from .models import *
from django.core.validators import RegexValidator

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
            tipoc = request.POST.get("tipoc")
            confirmar_senha = request.POST.get("confirmar_senha")
            
            dados_preenchidos = {'nome_preenchido' : nome,
                            'telefone_preenchido' : telefone,
                            'data_preenchida' : data,
                            'funcao_preenchida' : funcao,
                            'numeroc_preenchido' : numeroc,
                            'nomec_preenchido' : nomec,
                            'quantidadec_preenchida' : quantidadec,
                            'tipoc_preenchida' : tipoc,
                            'cpf_preenchido' : cpf,
                            'data_preenchida' : data}
        
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
                return render(request, 'home.html')

    except ValueError:
        return render(request, 'cadastro.html', dados_preenchidos)
            
    return render(request,"cadastro.html")

def home(request):
    render(request, "home.html")
    