from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

class Usuario(AbstractUser, PermissionsMixin):
# Informações principais do usuário
    username = models.CharField(max_length=255, unique=False)
    data_nasc = models.DateField()
    cpf = models.CharField(max_length=11, null=False, unique=True)
    telefone = models.CharField(max_length=13, unique=True, null=False)
    funcao = models.CharField(max_length=70, choices=[("levantador", "Levantador"),("atacante1","Atacante 1 (Ponteiro)"),
                                                      ("atacante2","Atacante 2 (Oposto)"),("defesa","Defesa (Líbero)")])

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ['username']

# Informações da camisa(número, nome, quantidade, tipo, tamanho)
    nomec = models.CharField(max_length=150, null=False)
    numeroc = models.IntegerField()
    quantidadec = models.IntegerField(choices=[(1,"1"),(2,"2"),(3,"3")])
    tipoc = models.CharField(max_length=70, choices=[("com", "Com manga"),("sem", "Sem manga")])
    tamanhoc = models.CharField(max_length=400, choices=[("pp","Tamanho PP = Dimensões: Altura 66 x Torax 46 x Quadril 46"),
                                                         ("p","Tamanho P = Dimensões: Altura 69 x Torax 48 x Quadril 48"),
                                                         ("m","Tamanho M = Dimensões: Altura 71 x Torax 52 x Quadril 52"),
                                                         ("g","Tamanho G = Dimensões: Altura 73 x Torax 55 x Quadril 55"),
                                                         ("gg","Tamanho GG = Dimensões: Altura 76 x Torax 59 x Quadril 59"),
                                                         ("xg","Tamanho XG = Dimensões: Altura 78 x Torax 62 x Quadril 62"),
                                                         ("exg","Tamanho EXG = Dimensões: Altura 83 x Torax 67 x Quadril 67")],
                                                         default="m")
    
    pagamento = models.CharField(max_length=50, default="Pendente" ,choices=[("pago","Pago"),("pendente","Pendente")], null=False)

class Registro(models.Model):
    nome = models.TextField(max_length=255)
    data_hora = models.DateTimeField(default = timezone.now)
    participantes = models.ManyToManyField(Usuario, related_name='jogos_inscritos', blank=True)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                             choices=[("aberto","Aberto"),
                                      ("andamento", "Em andamento"),
                                      ("finalizado","Finzalizado")],
                             default="aberto"
                            )
    
    placarA = models.PositiveIntegerField(default=0)
    placarB = models.PositiveIntegerField(default=0)
    vencedor = models.CharField(
        max_length=1,
        choices = [("A","Time A"),("B","Time B")],
        null=True, blank=True)
                            
class Partida(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)
    time = models.CharField(max_length=1, choices=[("A", "Time A"),("B", "Time B")])
    venceu = models.CharField(max_length=1, choices=[("A", "Time A"),("B", "Time B")])
    pontos = models.IntegerField(default=0)

class Inscrito(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Registro, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(default=timezone.now)

class Log(models.Model):
    data_hora = models.DateField(default = timezone.now)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    jogo = models.IntegerField(null=True, blank=True)
    acao = models.TextField(max_length=255)