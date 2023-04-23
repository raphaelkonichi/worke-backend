from django.shortcuts import render
from datetime import datetime as dt, timedelta
from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from workeApp.models import Exercicio_realizado, Exercicio_usuario, Usuario, Empresa, Plano, Peso_usuario, Grupo, Usuario_grupo, Exercicio
from workeApp.serializer import ExercicioSerializer, UsuarioSerializer, EmpresaSerializer, PlanoSerializer, Peso_usuarioSerializer, GrupoSerializer, Usuario_grupoSerializer, Exercicio_realizadoSerializer
from workeApp.utils import id_generator
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

class TodasEmpresasViewSet(APIView):

    def get(self, request):
        empresas = Empresa.objects.all()

        serializer = EmpresaSerializer(empresas, many=True)

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
        
        response = Response()
        response.data = ({
            "id": empresa.id,
            "nome": empresa.nome,
            "email": empresa.email,
            "cnpj": empresa.cnpj,
            "telefone": empresa.telefone,
            "data_criacao": empresa.data_criacao,
            "qtd_usuarios": Usuario.objects.filter(empresa__isnull=False).count(),
            "funcionarios_ativos_30dias": Usuario.objects.filter(data_ultimo_acesso__lte=dt.today(), data_ultimo_acesso__gt=dt.today()-datetime.timedelta(days=30)).filter(empresa__isnull=False).count(),
            "total_de_salas": Grupo.objects.all().count()
        })
        # serializer = EmpresaSerializer(empresa)

        # return Response(serializer.data)
        return response
    
    def delete(self, request, pk=None):
        empresa = Empresa.objects.filter(id=pk)
        
        if not empresa:
            return Response('Empresa não encontrada!')

        empresa.delete()
        return Response('Empresa excluída com sucesso!')

    def patch(self, request, pk=None):
        empresa = Empresa.objects.filter(id=pk)
        serializer = EmpresaSerializer(empresa, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(code=201, data=serializer.data)

        return Response(code=400, data="Dados incorretos!")

class ExercicioViewSet(APIView):

    def get(self, request):
        exercicios = Exercicio.objects.all()
        for item in exercicios:
            item.categoria = item.get_categoria_display()
        serializer = ExercicioSerializer(exercicios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExercicioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response("Dados incorretos!")
    
class ExercicioCategoriaViewSet(APIView):
    def get(self, request, pk=None):
        print(pk)
        exercicios = Exercicio.objects.filter(categoria=pk)
        for item in exercicios:
            item.categoria = item.get_categoria_display()
        serializer = ExercicioSerializer(exercicios, many=True)
        return Response(serializer.data)
    
class CategoriaViewSet(APIView):
    def get(self, request):
        categorias = []
        for c in Exercicio.categoria.field.choices:
            categorias.append({'id': c[0], 'nome': c[1]})

        print(categorias)
        # serializer = ExercicioSerializer(exercicios, many=True)
        return Response(categorias)

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

    def get(self, request, pk=None):
        # token = request.COOKIES.get('jwt')

        # if not token:
        #     raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Não foi possível realizar a autenticação!')

        peso_usuario = Peso_usuario.objects.filter(usuario_id=pk).order_by('data_medicao')
        serializer = Peso_usuarioSerializer(peso_usuario, many=True)

        return Response(serializer.data)

    def post(self, request, pk=None):
        usuario = Usuario.objects.filter(id=pk).first()

        serializer = Peso_usuarioSerializer(data=request.data)
        serializer.save()

        id = serializer.data['id']
        usuario_peso = Peso_usuario.objects.get(id=id)
        usuario_peso.usuario = usuario

        usuario_peso.save()
        updatedserializer = Peso_usuarioSerializer(usuario_peso)

        return Response(updatedserializer.data)
    
class ExercicioUsuarioViewSet(APIView):
    def get(self, request, pk=None):
        exercicios = Exercicio_realizado.objects.filter(usuario_id=pk).values('exercicio').annotate(quantidade = Count('exercicio')).order_by('-quantidade')
        for item in exercicios:
            exercicio = Exercicio.objects.filter(id=item['exercicio']).first()
            item['exercicio'] = exercicio.nome
            item['categoria'] = exercicio.get_categoria_display()
        return Response(exercicios)
    
    def post(self, request, pk=None):
        usuario = Usuario.objects.get(id=pk)
        exercicio = Exercicio.objects.filter(id=request.data['exercicio']).first()

        serializer = Exercicio_realizado(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        id = serializer.data['id']
        exercicio_realizado = Exercicio_realizado.objects.get(id=id)
        exercicio_realizado.usuario = usuario
        exercicio_realizado.exercicio = exercicio
        exercicio_realizado.save()

        updatedserializer = UsuarioSerializer(usuario)
        return Response(updatedserializer.data)
    
class RegisterView(APIView):
    def post(self, request):
        print("data",request.data)
        serializer = UsuarioSerializer(data=request.data)
        serializer.is_valid()
        print(serializer.errors)
        if serializer.errors:
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        usuario = Usuario.objects.filter(email=email).first()

        if usuario is None:
            return Response('Email inválido!')

        if not usuario.check_password(password):
            return Response('Senha incorreta!')

        payload = {
            "id": usuario.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)        

        serializer = UsuarioSerializer(usuario)

        response.data = ({
            'jwt': token,
            'usuario': serializer.data
        })

        print(response.data)

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
            
    def post(self, request, pk=None):
        usuario = Usuario.objects.filter(id=pk).first()
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response("Dados incorretos!")
        
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
            return Response(data=serializer.data)

        return Response("Dados incorretos!")
        
    def delete(self, request, pk=None):
        grupo = Grupo.objects.filter(id=pk).first()
        
        if not grupo:
            return Response('Usuário não encontrado!')

        grupo.delete()
        return Response('Usuário excluído com sucesso!')
    
class GrupoCodigoView(APIView):
    def get(self, request, pk=None):
        grupo = Grupo.objects.filter(codigo=pk).first()

        if not grupo:
            return Response('')

        serializer = GrupoSerializer(grupo)

        return Response(serializer.data)
            
    def patch(self, request, pk=None):
        grupo = Grupo.objects.filter(codigo=pk).first()
        serializer = GrupoSerializer(grupo, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

        return Response(data="Dados incorretos!")
        
    def delete(self, request, pk=None):
        grupo = Grupo.objects.filter(codigo=pk).first()
        
        if not grupo:
            return Response('Usuário não encontrado!')

        grupo.delete()
        return Response('Usuário excluído com sucesso!')
        
class CriarGrupoViewSet(APIView):
    def post(self, request, pk=None):
        usuario = Usuario.objects.filter(id=pk).first()

        serializer = GrupoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        id = serializer.data['id']
        grupo = Grupo.objects.get(id=id)
        grupo.admin = usuario

        grupo.save()
        updatedserializer = GrupoSerializer(grupo)
        return Response(updatedserializer.data)

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

class DashboardFuncionarioView(APIView):
    def get(self, request):
        return Response(Usuario.objects.filter(empresa__isnull=False).count())

class DashboardFuncionario30DiasView(APIView):
    def get(self, request):
        return Response(Usuario.objects.filter(data_ultimo_acesso__lte=dt.today(), data_ultimo_acesso__gt=dt.today()-datetime.timedelta(days=30)).filter(empresa__isnull=False).count())

class DashboardPontuacaoTotalSalaView(APIView):
    def get(self, request, pk=None):
        grupoobj = Grupo.objects.filter(id=pk).first()
        return Response(Usuario_grupo.objects.filter(grupo=grupoobj).aggregate(Sum('pontuacao')))

class DashboardTotalSalasView(APIView):
    def get(self, request):
        return Response(Grupo.objects.all().count())

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
            'jwt': token,
            "id": empresa.id
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
