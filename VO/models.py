from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
# Informações principais do usuário
    nome = models.CharField(max_length=300, null=False)
    telefone = models.CharField(max_length=13, unique=True, null=False)
    senha = models.CharField(max_length=250, null=False)
    funcao = models.CharField(max_length=70, choices=[("levantador", "Levantador"),("atacante1","Atacante 1 (Ponteiro)"),
                                                      ("atacante2","Atacante 2 (Oposto)"),("defesa","Defesa (Líbero)")])

# Informações da camisa
    nomec = models.CharField(max_length=150, null=False)
    numeroc = models.IntegerField()
    quantidadec = models.IntegerField(choices=[("1","1"),("2","2"),("3","3")])
    tipoc = models.CharField(max_length=70, choices=[("com", "Com manga"),("sem", "Sem manga")])
    tamanhoc = models.CharField(max_length=400, choices=[("pp","Tamanho PP = Dimensões: Altura 66 x Torax 46 x Quadril 46"),
                                                         ("p","Tamanho P = Dimensões: Altura 69 x Torax 48 x Quadril 48"),
                                                         ("m","Tamanho M = Dimensões: Altura 71 x Torax 52 x Quadril 52"),
                                                         ("g","Tamanho G = Dimensões: Altura 73 x Torax 55 x Quadril 55"),
                                                         ("gg","Tamanho GG = Dimensões: Altura 76 x Torax 59 x Quadril 59"),
                                                         ("xg","Tamanho XG = Dimensões: Altura 78 x Torax 62 x Quadril 62"),
                                                         ("exg","Tamanho EXG = Dimensões: Altura 83 x Torax 67 x Quadril 67")])
    