from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MedicoManager(BaseUserManager):
    """
    Gerenciador de usuários personalizados para o modelo Medico.
    """
    def create_user(self, cpf, password, **extra_fields):
        """
        Cria e salva um novo médico.
        """
        if not cpf:
            raise ValueError(_('O CPF é obrigatório'))
        if not extra_fields.get('crm'):
            raise ValueError(_('O CRM é obrigatório'))
        cpf = self.normalize_email(cpf)  # Use normalize_email para formatar o CPF (opcional)
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password, **extra_fields):
        """
        Cria e salva um novo superusuário médico.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário precisa ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário precisa ter is_superuser=True.'))

        return self.create_user(cpf, password, **extra_fields)

class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Medico(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário Medico.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)  # Corrigido para EmailField e opcional
    data_de_nascimento = models.DateField(default=timezone.now)
    cpf = models.CharField(max_length=11, unique=True)  #Removido null=False, blank=True. CPF deve ser obrigatório.
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, blank=True, null=True) # Relacionamento com Especialidade
    password = models.CharField(max_length=128)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'crm', 'password']

    objects = MedicoManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='medico_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='medico_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.nome