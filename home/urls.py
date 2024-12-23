from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('login/', views._login_, name='login'),
    #path('adm/', views.view, name='adm'),
    #path('teste/', views.teste, name='teste'),
    ]