from rest_framework import serializers
from workeApp.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','nome','sobrenome','email','senha','cpf','telefone','genero','data_nascimento','data_criacao','altura','freq_exercicios','tipo_usuario','pontuacao','nivel','imagem','primeiro_acesso','plano']