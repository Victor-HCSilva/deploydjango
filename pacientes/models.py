from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.
class PacienteManager(BaseUserManager):
    """
    Gerenciador de usuários personalizados para o modelo Paciente.
    """
    def create_user(self, cpf, password, **extra_fields):
        """
        Cria e salva um novo usuário.
        """
        if not cpf:
            raise ValueError(_('O CPF é obrigatório'))
        cpf = self.normalize_email(cpf)  # Use normalize_email para formatar o CPF (opcional)
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password, **extra_fields):
        """
        Cria e salva um novo superusuário.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário precisa ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário precisa ter is_superuser=True.'))

        return self.create_user(cpf, password, **extra_fields)

class Paciente(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário Paciente.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z\s]+$',
                message='O nome deve conter apenas letras e espaços.',
                code='invalid_name'
            )
        ]
    )
    email = models.EmailField(
        max_length=100, 
        unique=True, 
        blank=False, 
        null=False
    )  # Email é obrigatório e validado
    data_de_nascimento = models.DateField(
        default=timezone.now,
        help_text=f'eg. {str(timezone.now().date())}'
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(
                14,
                message='O CPF deve ter 14 dígitos .'  
            )
        ]
    )
    password = models.CharField(
        max_length=25,
        unique=True,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(
                8,
                message='A senha deve ter pelo menos 8 dígitos.'  
            )
        ]
    )
    # Adiciona os campos is_staff e is_superuser
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'cpf'  # Define o CPF como o campo de identificação principal
    REQUIRED_FIELDS = ['email', 'password']  # Email agora é opcional

    objects = PacienteManager()

    # Corrige o problema de nomes conflitantes com related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='paciente_set',  # Nome exclusivo para o relacionamento do Paciente
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='paciente_permissions_set',  # Nome exclusivo para o relacionamento do Paciente
        blank=True
    )

    def __str__(self):
        return self.nome

