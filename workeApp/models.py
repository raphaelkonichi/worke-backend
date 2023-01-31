from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class Plano(models.Model):
    nome = models.CharField(max_length=50)
    data_criacao = models.DateField(default=datetime.date.today)
    valor = models.DecimalField(max_digits=3, decimal_places=2)
    instrument = models.CharField(max_length=100)
    max_participantes = models.IntegerField()

    def __str__(self):
        return self.nome

class Empresa(models.Model):
    nome = models.CharField(max_length=80)
    cnpj = models.CharField(max_length=14)
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    telefone = models.CharField(max_length=11)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, null=True)
    data_criacao = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.nome

class Exercicio(models.Model):
    CATEGORIAS = ( 
        # ('S', 'Small'),
        # ('M', 'Medium'),
        # ('L', 'Large'),
    )
    nome = models.CharField(max_length=80)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS)
    data_criacao = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.nome

class Expectativas(models.Model):
    descricao = models.CharField(max_length=50)
    data_criacao = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.descricao

class Usuario(AbstractUser):
    GENEROS = ( 
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )
    FREQUENCIA = ( 
        # Frequencia dos exercicios
        # ('M', 'Masculino'),
        # ('F', 'Feminino'),
        # ('O', 'Outros'),
    )
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=80)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default="password")
    cpf = models.CharField(max_length=11, null=True)
    telefone = models.CharField(max_length=11, null=True)
    genero = models.CharField(max_length=1, choices=GENEROS, null=True)
    data_nascimento = models.DateField(null=True)
    data_criacao = models.DateField(default=datetime.date.today)
    data_ultimo_acesso = models.DateField(default=datetime.date.today)
    altura = models.IntegerField(null=True)
    freq_exercicios = models.CharField(max_length=1, choices=FREQUENCIA, null=True)
    # expectativas = models.ManyToManyField(Expectativas, null=True)
    tipo_usuario = models.CharField(max_length=1, null=True)
    pontuacao = models.IntegerField(null=True)
    nivel = models.IntegerField(null=True)
    imagem = models.BinaryField(null=True)
    primeiro_acesso = models.BooleanField(default=False)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nome

class Exercicio_usuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    data_criacao = models.DateField(default=datetime.date.today)
    favorito = models.BooleanField(default=False)

    def __str__(self):
        return self.data_criacao

class Exercicio_realizado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    data_criacao = models.DateField(default=datetime.date.today)
    pontuacao = models.IntegerField()
    duracao = models.IntegerField()

    def __str__(self):
        return self.data_criacao

class Peso_usuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateField(default=datetime.date.today)
    data_medicao = models.DateField()
    peso = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.peso

class Grupo(models.Model):
    titulo = models.CharField(max_length=50)
    codigo = models.CharField(max_length=4)
    senha = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    admin = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    qtd_participantes = models.IntegerField()
    data_criacao = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.titulo

class Usuario_grupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pontuacao = models.IntegerField()
    posicao_ranking = models.IntegerField()
    data_criacao = models.DateField(default=datetime.date.today) 
    data_posicao  = models.DateField()

    def __str__(self):
        return self.data_criacao
