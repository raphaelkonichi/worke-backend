from django.contrib import admin
from workeApp.models import Usuario
# Register your models here.

class Usuario(admin.ModelAdmin):
    list_display = ('id','nome','sobrenome','email','senha','cpf','telefone','genero','data_nascimento','data_criacao','altura','freq_exercicios','tipo_usuario','pontuacao','nivel','imagem','primeiro_acesso','plano')
    list_display_links = ('id', 'nome')
    search_fields = ('nome')

