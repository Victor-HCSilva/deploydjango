from rest_framework import serializers
from pacientes.models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__' 
        # ou especifique os campos específicos que você deseja "serializar"
        extra_kwargs = {
            'id': {'required': True},
            'nome': {'required': True},
            'email': {'required': True},
            'data_de_nascimento': {'required': True},
            'cpf': {'required': True},
            'password': {'required': True},
        } 

