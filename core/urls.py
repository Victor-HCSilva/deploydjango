from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Inclui as URLs do 'home'
    #path('login/', include('login.urls')),  # Inclui as URLs do 'login'
    path('portal_do_paciente/', include('portal_do_paciente.urls')),  # Inclui as URLs do 'portal_do_paciente'
    path('agendamentos/', include('agendamentos.urls'))

]