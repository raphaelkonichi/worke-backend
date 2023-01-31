from rest_framework import serializers
from workeApp.models import Usuario, Empresa, Plano, Peso_usuario, Grupo, Usuario_grupo

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','nome','sobrenome','email','password','cpf','telefone','genero','data_nascimento','data_criacao','altura','freq_exercicios','tipo_usuario','pontuacao','nivel','primeiro_acesso','plano','empresa']
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

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id','nome','email','senha','cnpj','telefone','data_criacao']
        
        extra_kwargs = {
            'senha': {'write_only': True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()

        return instance

class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id','nome','valor','instrument','max_participantes']
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()

        return instance

class Peso_usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peso_usuario
        fields = ['usuario', 'data_criacao', 'data_medicao', 'peso']
            
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()

        return instance


class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id','titulo','codigo','senha','empresa','admin','qtd_participantes','data_criacao']
        
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()

        return instance

class Usuario_grupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id','grupo','usuario','pontuacao','posicao_ranking','data_criacao','data_posicao']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()

        return instance        