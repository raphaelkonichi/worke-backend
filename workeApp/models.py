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
        ('BRA', 'Braços e ombros'),
        ('PES', 'Pescoço'),
        ('PUN', 'Punho e dedos'),
        ('COS', 'Costas e tronco'),
        ('PER', 'Pernas'),
    )
    nome = models.CharField(max_length=80)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS)
    duracao = models.IntegerField(default=15)
    pontuacao = models.IntegerField(default=100)
    data_criacao = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.nome

class Expectativas(models.Model):
    descricao = models.CharField(max_length=50)
    data_criacao = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.descricao

class Usuario(AbstractUser):
    GENDER = ( 
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )
    FREQUENCY = ( 
        (1, 'Iniciante'),
        (2, 'Intermediário'),
        (3, 'Avançado'),
    )
    first_name = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default="password")
    # cpf = models.CharField(max_length=11, null=True)
    # telefone = models.CharField(max_length=11, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True)
    birth_date = models.DateField(null=True)
    create_date = models.DateField(default=datetime.date.today)
    date_last_access = models.DateField(default=datetime.date.today)
    height = models.CharField(max_length=3,null=True)
    frequency = models.CharField(max_length=15, choices=FREQUENCY, null=True)
    # expectativas = models.ManyToManyField(Expectativas, null=True)
    user_type = models.CharField(max_length=1, null=True)
    points = models.IntegerField(default=0)
    consecutive_days = models.IntegerField(null=True)
    qty_exercises = models.IntegerField(null=True)
    total_minutes = models.IntegerField(null=True)
    level = models.IntegerField(default=1)
    image = models.TextField(null=True)
    first_access = models.BooleanField(default=False)
    plan = models.ForeignKey(Plano, on_delete=models.CASCADE, null=True)
    enterprise = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    weight = models.CharField(max_length=3,null=True)
    expectations = models.CharField(max_length=255, null=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

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
    pontuacao = models.IntegerField(default=100)
    duracao = models.IntegerField(default=15)

    def __str__(self):
        return str(self.data_criacao)

class Peso_usuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateField(default=datetime.date.today)
    data_medicao = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.peso

class Grupo(models.Model):
    titulo = models.CharField(max_length=50, null=True)
    codigo = models.CharField(max_length=4, null=True)
    senha = models.CharField(max_length=50, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    qtd_participantes = models.IntegerField(default=5)
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
