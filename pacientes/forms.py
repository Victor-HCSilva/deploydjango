from django import forms
from django.utils import timezone
from django.utils.timezone import timedelta
from pacientes.models import Paciente

def validate_future_date(value):
    """Valida se a data é no futuro"""
    if value > timezone.now().date():
        raise forms.ValidationError("A data não pode ser no futuro.")
    return value

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'email', 'data_de_nascimento', 'cpf', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'data_de_nascimento': forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
        }

        data_de_nascimento = forms.DateField(
            widget=forms.DateInput(
                format="%Y-%m-%d",
                attrs={'type': 'date'}
            ),
            input_formats=["%Y-%m-%d"],
            validators=[validate_future_date],
        )


    cpf = forms.CharField(label="CPF", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Senha")