from django.shortcuts import render
from rest_framework import viewsets
from workeApp.models import Usuario
from workeApp.serializer import UsuarioSerializer
# Create your views here.

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

