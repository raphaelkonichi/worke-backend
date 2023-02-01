"""worke_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from workeApp.views import UsuariosViewSet, RegisterView, LoginView, LogoutView, EmpresaViewSet, LoginEmpresaView, RegisterEmpresaView, FuncionarioView, EmpresaFuncionarioView, GrupoView, EmpresaGrupoView, GrupoFuncionarioView, DashboardFuncionarioView, DashboardFuncionario30DiasView, DashboardTotalSalasView, DashboardPontuacaoTotalSalaView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', UsuariosViewSet.as_view()),
    path('empresa/', EmpresaViewSet.as_view()),
    path('empresa/<int:pk>', EmpresaViewSet.as_view()),
    path('register', RegisterView.as_view()),
    path('registerEmpresa', RegisterEmpresaView.as_view()),
    path('empresaFuncionario/<int:pk>', EmpresaFuncionarioView.as_view()),
    path('empresaGrupo/<int:pk>', EmpresaGrupoView.as_view()),
    path('funcionario/<int:pk>', FuncionarioView.as_view()),
    path('dashboardFuncionario/', DashboardFuncionarioView.as_view()),
    path('dashboardFuncionario30Dias/', DashboardFuncionario30DiasView.as_view()),
    path('dashboardTotalSalas/', DashboardTotalSalasView.as_view()),
    path('dashboardPontuacaoTotalSalaView/<int:pk>', DashboardPontuacaoTotalSalaView.as_view()),
    path('grupo/<int:pk>', GrupoView.as_view()),
    path('grupoFuncionario/<int:pk>', GrupoFuncionarioView.as_view()),
    path('login', LoginView.as_view()),
    path('loginEmpresa', LoginEmpresaView.as_view()),
    path('logout', LogoutView.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
