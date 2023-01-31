from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from workeApp.models import Usuario, Empresa, Plano, Peso_usuario, Grupo, Usuario_grupo
from workeApp.serializer import UsuarioSerializer, EmpresaSerializer, PlanoSerializer, Peso_usuarioSerializer, GrupoSerializer, Usuario_grupoSerializer
import jwt, datetime

# Create your views here.

class UsuariosViewSet(APIView):

    def get(self, request, *args, **kwargs):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')
        
        usuario = None

        try:
            id = request.query_params["id"]
            if id is not None:
                usuario = Usuario.objects.filter(id=id)
                serializer = UsuarioSerializer(usuario, many=True)
        except:
            None
        try:
            nome = request.query_params["nome"]
            if nome is not None:
                usuario = Usuario.objects.filter(nome__icontains=nome)
                serializer = UsuarioSerializer(usuario, many=True)
        except:
            None
        try:
            email = request.query_params["email"]
            if email is not None:
                usuario = Usuario.objects.filter(email__icontains=email)
                serializer = UsuarioSerializer(usuario, many=True)
        except:
            None

        if usuario is None:
            usuario = Usuario.objects.all()
            serializer = UsuarioSerializer(usuario, many=True)

        return Response(serializer.data)

class EmpresaViewSet(APIView):

    def get(self, request, pk=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        empresa = Empresa.objects.filter(id=payload['id']).first()
        serializer = EmpresaSerializer(empresa)

        return Response(serializer.data)
    
    def delete(self, request, pk=None):
        empresa = Empresa.objects.filter(id=pk)
        
        if not empresa:
            return Response('Empresa não encontrada!')

        empresa.delete()
        return Response('Empresa excluída com sucesso!')

class PlanoViewSet(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        plano = Plano.objects.filter(id=payload['id']).first()
        serializer = PlanoSerializer(plano)

        return Response(serializer.data)

    def post(self, request):
        serializer = PlanoSerializer(data=request.data)
        serializer.save()
        return Response(serializer.data)

class PesoUsuarioViewSet(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        peso_usuario = Peso_usuario.objects.filter(id=payload['id']).first()
        serializer = Peso_usuarioSerializer(peso_usuario)

        return Response(serializer.data)

    def post(self, request):
        serializer = Peso_usuarioSerializer(data=request.data)
        serializer.save()
        return Response(serializer.data)

class RegisterView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        usuario = Usuario.objects.filter(email=email).first()

        if usuario is None:
            raise AuthenticationFailed('Usuário não encontrado!')

        if not usuario.check_password(password):
            raise AuthenticationFailed('Senha incorreta!')

        payload = {
            "id": usuario.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)        

        response.data = ({
            'jwt': token
        })

        return response

class RegisterEmpresaView(APIView):
    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class EmpresaFuncionarioView(APIView):
    def post(self, request, pk=None):

        empresaobj = Empresa.objects.filter(id=pk).first()

        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        id = serializer.data['id']
        usuario = Usuario.objects.get(id=id)
        usuario.empresa = empresaobj
        usuario.save()

        updatedserializer = UsuarioSerializer(usuario)
        return Response(updatedserializer.data)

    def get(self, request, pk=None):
        empresaobj = Empresa.objects.filter(id=pk).first()

        usuarios = Usuario.objects.filter(empresa=empresaobj)
        serializer = UsuarioSerializer(usuarios, many=True)

        return Response(serializer.data)

class FuncionarioView(APIView):
    def get(self, request, pk=None):
        usuario = Usuario.objects.filter(id=pk).first()
        serializer = UsuarioSerializer(usuario)

        return Response(serializer.data)
            
    def patch(self, request, pk=None):
        usuario = Usuario.objects.filter(id=pk).first()
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(code=201, data=serializer.data)

        return Response(code=400, data="Dados incorretos!")
        
    def delete(self, request, pk=None):
        usuario = Usuario.objects.filter(id=pk)
        
        if not usuario:
            return Response('Usuário não encontrado!')

        usuario.delete()
        return Response('Usuário excluído com sucesso!')

class GrupoView(APIView):
    def get(self, request, pk=None):
        grupo = Grupo.objects.filter(id=pk).first()
        serializer = GrupoSerializer(grupo)

        return Response(serializer.data)
            
    def patch(self, request, pk=None):
        grupo = Grupo.objects.filter(id=pk).first()
        serializer = GrupoSerializer(grupo, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(code=201, data=serializer.data)

        return Response(code=400, data="Dados incorretos!")
        
    def delete(self, request, pk=None):
        grupo = Grupo.objects.filter(id=pk).first()
        
        if not grupo:
            return Response('Usuário não encontrado!')

        grupo.delete()
        return Response('Usuário excluído com sucesso!')
        
class EmpresaGrupoView(APIView):
    def post(self, request, pk=None):

        empresaobj = Empresa.objects.filter(id=pk).first()

        serializer = GrupoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        id = serializer.data['id']
        grupo = Grupo.objects.get(id=id)
        grupo.empresa = empresaobj
        grupo.save()

        updatedserializer = GrupoSerializer(grupo)
        return Response(updatedserializer.data)
        
    def get(self, request, pk=None):
        empresaobj = Empresa.objects.filter(id=pk).first()

        grupo = Grupo.objects.filter(empresa=empresaobj)
        serializer = GrupoSerializer(grupo, many=True)

        return Response(serializer.data)
                
class GrupoFuncionarioView(APIView):        
    def get(self, request, pk=None):
        grupoobj = Grupo.objects.filter(id=pk).first()

        funcionarios = Usuario_grupo.objects.filter(grupo=grupoobj).order_by('-pontuacao')
        serializer = Usuario_grupoSerializer(funcionarios, many=True)

        return Response(serializer.data)

class LoginEmpresaView(APIView):
    def post(self, request):
        email = request.data['email']
        senha = request.data['senha']

        empresa = Empresa.objects.filter(email=email).first()

        if empresa is None:
            raise AuthenticationFailed('Empresa não encontrada!')

        if empresa.senha != senha:
            raise AuthenticationFailed('Senha incorreta!')

        payload = {
            "id": empresa.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)        

        response.data = ({
            'jwt': token
        })

        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout realizado com sucesso!'
        }

        return response
