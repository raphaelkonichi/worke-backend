from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from workeApp.models import Usuario, Empresa
from workeApp.serializer import UsuarioSerializer, EmpresaSerializer
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

    def get(self, request):
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

class LoginEmpresaView(APIView):
    def post(self, request):
        email = request.data['email']
        senha = request.data['senha']

        empresa = Empresa.objects.filter(email=email).first()

        if empresa is None:
            raise AuthenticationFailed('Empresa não encontrada!')

        # if not empresa.check_password(senha):
        #     raise AuthenticationFailed('Senha incorreta!')

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
