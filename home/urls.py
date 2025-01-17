from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('login/', views.login_, name='login'),
    #path('adm/', views.view, name='adm'),
    #path('teste/', views.teste, name='teste'),
    ]