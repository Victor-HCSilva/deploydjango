#from django.db import models
from rest_framework import generics
#from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from pacientes.models import Paciente
from .serializers import PacienteSerializer
from rest_framework.pagination import PageNumberPagination 

# --------------------------------------------------------------------
# View para listar e criar consultas (com paginação, busca e ordenação)
class PacienteListView(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    #pagination_class = PageNumberPagination
    #pagination_class.page_size = 2  # Define o tamanho da página
    filter_backends = [SearchFilter, OrderingFilter]  # Define os filtros
    search_fields = ['nome', 'cpf', 'data_de_nascimento','email']  # Campos para busca
    ordering_fields = ['data_de_nascimento', 'nome','id']  # Campos para ordenação

# --------------------------------------------------------------------
# View para visualizar, atualizar e excluir consultas
class PacienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

# --------------------------------------------------------------------
# View para criar consultas
class PacienteCreateView(generics.CreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class CustomPagination(PageNumberPagination):
    page_size = 2  # Define o tamanho da página
    page_size_query_param = 'page_size'  # Parâmetro para alterar o tamanho da página