from django import forms
from .models import Medico
from . import tratamento

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
        }
        labels = {
            'cpf': 'CPF',
            'password': 'Senha',
            'crm':'CRM',
        }

    def clean_cpf(self):
        """Limpa e valida o campo CPF."""
        cpf = self.cleaned_data.get('cpf', '')
        print(f"CPF antes da formatação: {cpf}")  # Debug: Imprime o CPF antes
        cpf = tratamento.formatar_cpf(cpf)
        print(f"CPF depois da formatação: {cpf}")  # Debug: Imprime o CPF depois


        if len(cpf) != 11 or not cpf.isdigit():
            raise forms.ValidationError("CPF inválido. Deve conter 11 dígitos numéricos.")
        return cpf