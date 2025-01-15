from . import views
from django.urls import path


urlpatterns = [
    path('<int:id>/', views.portal_do_paciente, name='portal_do_paciente'), 
    path('<int:id>/cadastro_de_medicos/', views.cadastro_de_medicos, name='cadastro_de_medicos'),
    path('<int:id>/gestao_de_pacientes/', views.gestao_de_pacientes, name='gestao_de_pacientes'),
    path('<int:id>', views.agendar_consulta, name='agendar_consulta'),
    path('logout/', views.logout_view, name='logout'),
    path('paciente/<int:id_adm>/<int:id_paciente>/editar/', views.editar_paciente, name='editar_paciente'),
    path('paciente/<int:id>/<int:id_adm>remover/', views.remover_paciente, name='remover_paciente'),
]