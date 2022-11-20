from rest_framework import serializers
from workeApp.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','nome','sobrenome','email','password','cpf','telefone','genero','data_nascimento','data_criacao','altura','freq_exercicios','tipo_usuario','pontuacao','nivel','imagem','primeiro_acesso','plano']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
