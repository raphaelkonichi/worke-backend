from django.db import models

# Create your models here.
class Plano(models.Model):
    nome = models.CharField(max_length=50)
    data_criacao = models.DateField()
    valor = models.DecimalField(max_digits=3, decimal_places=2)
    instrument = models.CharField(max_length=100)
    max_participantes = models.IntegerField(max_digits=11)

    def __str__(self):
        return self.name

class Empresa(models.Model):
    nome = models.CharField(max_length=80)
    cnpj = models.CharField(max_length=14)
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    telefone = models.CharField(max_length=11)
    plano_id = models.ForeignKey(Plano, on_delete=models.CASCADE)
    data_criacao = models.DateField()

    def __str__(self):
        return self.name

class Exercicio(models.Model):
    CATEGORIAS = ( 
        # ('S', 'Small'),
        # ('M', 'Medium'),
        # ('L', 'Large'),
    )
    nome = models.CharField(max_length=80)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS)
    data_criacao = models.DateField()

    def __str__(self):
        return self.name

class Expectativas(models.Model):
    descricao = models.CharField(max_length=50)
    data_criacao = models.DateField()

    def __str__(self):
        return self.name

class Usuario(models.Model):
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
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    genero = models.CharField(max_length=1, choices=GENEROS)
    data_nascimento = models.DateField()
    data_criacao = models.DateField()
    altura = models.IntegerField(max_digits=3)
    freq_exercicios = models.CharField(max_length=1, choices=FREQUENCIA)
    expectativas = models.ManyToManyField(choices=Expectativas)
    tipo_usuario = models.CharField(max_length=1)
    pontuacao = models.IntegerField(max_digits=11)
    nivel = models.IntegerField(max_digits=11)
    imagem = models.BinaryField()
    primeiro_acesso = models.BooleanField(default=False)
    plano_id = models.ForeignKey(Plano, on_delete=models.CASCADE)

    def __str__(self):
        return self.name