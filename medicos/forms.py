from django import forms
from .models import Medico, Especialidade

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'email', 'data_de_nascimento', 'cpf', 'crm', 'especialidade', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'data_de_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'crm': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            #Adicione outros widgets se necessario

        }
        labels = {
            'cpf': 'CPF',
            'password': 'Senha',
            'crm':'CRM',
            #Adicione outros labels se necessario
        }