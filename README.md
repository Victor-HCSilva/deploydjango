# Projeto Integrador FAP: Sistema de Agendamento e Gerenciamento de Consultas para JA Serviços Médicos LTDA (SAGe)

- Resumo: O SAGe é um sistema web desenvolvido em Python e Django para agendamento de consultas e gerenciamento de pacientes para a clínica médica JA Serviços Médicos LTDA. A plataforma proporcionará aos pacientes uma maneira fácil e
intuitiva de agendar consultas online, enquanto oferece à clínica uma ferramenta eficiente para organizar horários, gerenciar informações de pacientes e otimizar o fluxo de atendimento.

## Funcionalidades Principais ##
* Cadastro de pacientes e médicos
* Edição de usuários
* Agendamento de consultas
* Visualização de consultas agendadas
* Sistema de exclusão e cancelamento de consultas

## Requisitos para rodar o projeto

### Setup de ambiente:

- [Python](https://docs.python.org/3/)
- [Django](https://docs.djangoproject.com/en/)

### Como rodar na minha máquina?

- Clone o projeto  `git clone https://github.com/gabriellgr/projeto-integrador.git`
- Crie um ambiente virtual:
    -  windows:  `python -m venv venv`
    - linux:  `python3 -m venv venv`
- Ative o ambiente virtual:
    - windows `.\venv\Scripts\activate`
    - linux `source venv/bin/activate`
- Instale os requisitos  `pip install -r requeriments.txt`
- Rode  `python manage.py migrate`
- Rode  `python manage.py createsuperuser` e cadastre seu usuário.

  Exemplo:
  ```
  Apelido/Usuário: admin
  E-mail: admin@email.com
  Password:
  Password (again):
  ```
- Inicie o servidor `python manage.py runserver`

Para visualizar se tudo está executando como o esperado, acesse o seguinte endereço: http://localhost:8000/


  ## Estrutura do projeto
  - `./core/` : É onde gerenciamos configurações e rotas do nosso projeto.
  - `./core/urls.py`: Configuramos nossas rotas.
  ``` Python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('home.urls')),  # Inclui as URLs do 'home'
        path('portal_do_paciente/', include('portal_do_paciente.urls')),  # Inclui as URLs do 'portal_do_paciente'
        path('agendamentos/', include('agendamentos.urls'))
    
    ]
  ``` 

## Arquivos urls.py (Rotas):
- home/urls.py:
    ```python
    from django.urls import path, include
    from . import views


    urlpatterns = [
        path('', views.home, name='home'),
        path('cadastro/', views.cadastro, name = 'cadastro'),
        path('login/', views._login_, name='login'),
    ]
    ```
- portal_do_paciente/urls.py
    ```python
    from . import views
    from django.urls import path

    urlpatterns = [
        path('<int:id>/', views.portal_do_paciente, name='portal_do_paciente'), 
        path('<int:id>/cadastro_de_medicos/', views.cadastro_de_medicos, name='cadastro_de_medicos'),
        path('<int:id>/gestao_de_pacientes/', views.gestao_de_pacientes, name='gestao_de_pacientes'),
        path('<int:id>', views.agendar_consulta, name='agendar_consulta'),
        path('logout/', views.logout_view, name='logout'),
        path('paciente/<int:id>/editar/', views.editar_paciente, name='editar_paciente'),
        path('paciente/<int:id>/remover/', views.remover_paciente, name='remover_paciente'),
    ]
    ```

## Banco de dados (revisar)

- Arquivos onde ficam as "tabelas" criadas com object relational model (ORM), neste projeto foi
utilizado o ORM nativo do Django. As principais tabelas criadas foram para os pacientes, medicos e 
o agendamentos. Ambos dividos por apps, com nomes: pacientes, medicos e agendamentos.

- A função destes models é simples, paciente: o usuário que utiliza o serviço
e pode solicitar agendamentos para si mesmo, medico: o profissional que ficará disponível 
para seleção e escolha do usuário (paciente). E por fim angendamentos é responsável por unir ambos
e gerenciar datas e horários de disponibilidade.

- As class que conmpõem o sistema de usuários/pacientes em pacientes/models.py, `PacienteManager` e `Paciente`:

- `class PacienteManager`:
    - Responsável pelos sistemas de permissões.

- `class Paciente`:
    - responsável junto da class PacienteManager inserir novos pacientes.

```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator

class PacienteManager(BaseUserManager):

    #...
    def create_user(self, cpf, password, **extra_fields):
    #...
    def create_superuser(self, cpf, password, **extra_fields):
    #...


class Paciente(AbstractBaseUser, PermissionsMixin):
    #...
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
    #...
```

- Estas classes permitem o uso deste formato de usuário (Paciente) no lugar o usuário padrão do Django (User), com a seguinte configuração: no arquivo core/settings.py. O que permite usar as permissões e outras funcionalidades customizadas.

```python
#Incluindo o modelo Paciente no AUTH_USER_MODEL
AUTH_USER_MODEL = 'pacientes.Paciente'
```



- A partir da class construida é possível criar o arquivo forms.py que recebe as classes e cria 
um formulário que pode ser passado ao arquivo html.

- Parte do arquivo forms.py da class Paciente:


```python
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
```

- O modelo responsável pelo cadastro de medicos esta em medicos/models.py:

```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MedicoManager(BaseUserManager):
    #...
    def create_user(self, cpf, password, **extra_fields):
    #...
    def create_superuser(self, cpf, password, **extra_fields):
    #...

class Medico(AbstractBaseUser, PermissionsMixin):
    #...
```
- Diferente da classes do arquivo `paciente/models.py` criados para serem usados como autenticação personalizado 
as class do arquivo `medicos/models.py` têm o objetivo único de adicionar profissionais a serem escolhidos pelos 
usuários.

- Após a criação dos modelos é necessário realizar novamente as migrações:

```cmd
    python manager.py makemigrations
```

```cmd
    python manager.py migrate
```

- A partir do campos da class é criado uma formulário que é passado ao template deste modo:

- `home/views.py`, função cadstro responsável pelo cadastro inicial:

```python
def cadastro(request):
    """
    View para cadastrar um novo paciente.
   """
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # Cria o novo paciente no banco de dados
            print(form)
            paciente = form.save(commit=False)  # Cria o objeto Paciente, mas não salva ainda
            
            # Define a senha usando set_password
            paciente.set_password(form.cleaned_data['password'])

            # Define a data de nascimento corretamente
            paciente.data_de_nascimento = form.cleaned_data['data_de_nascimento']
            
            # Salva o paciente no banco de dados
            paciente.is_staff = False
            paciente.is_superuser = False
            paciente.is_active = True
    
            paciente.save()

            # Faz o login do paciente recém-cadastrado
            login(request, paciente) 
            messages.success(request, 'Paciente cadastrado com sucesso!')

            return redirect('login')  # Redireciona para a página inicial após o cadastro
        else:
            # Imprime os erros do formulário para debugging
            print(form.errors)
            return render(request, 'cadastro.html', {'form': form})
    else:
        form = PacienteForm()
    return render(request, 'cadastro.html', {'form': form})
```

- No arquivo cadastro.html:

```html
<form method="POST" class="form-group">{% csrf_token %}
    {% for field in form %}
        <div class="form-group">
        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
        {{ field }}
        {% if field.errors %}
            <ul class="errors">
            {% for error in field.errors %}
                <li class="text-danger">{{ error }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Cadastrar</button>
</form>
```

- Vale ressaltar que não é o único modo de fazer cadastro com o Django, é possível
fazer um formulario tradicional com html e recebendo os valores na função após a submição.

## Arquivos  que 'renderizam' o template:

- home/views.py;
- portal_do_paciente/views.py;

- Cada função têm como objetivo primário passar qual arquivo *.html* deve ser exibido,
o "nome" dado (rota) estão localizados no arquivos urls.py. As rotas devem ser exibidas em seu navegador
http://127.0.0.1:8000/portal_do_paciente/

```python
return render(request, 'portal_do_paciente.html', context)
```

- Também é possível passar viariáveis python para o template o que forneçe
dinâmica e versátilidade.

```python
     #Variaves passadas ao template
    context = {
        'paciente': paciente,  # Adicione o objeto paciente ao contexto
        'data':DATA, # Data
        'admin': IS_ADMIN,
        'name': FIRST_NAME,
        'medicos':medicos,
        'agendamentos':agendamentos,
    }
```

- Essas variáveis são acessadas com uma linguagem específica
que mistura python ao arquivo html. Exemplo em portal_do_paciente/templates/portal_do_paciente.html:

```html
{% for medico in medicos %}
    <tr>
        <td>{{ medico.nome }}</td>
        <td>{{ medico.especialidade }}</td>
        <td>{{ medico.crm }}</td>
    </tr>
{% endfor %}
```

## As páginas web (arquivos .html)
- ` Divididas nas pastas home/templates e portal_do_paciente/templates `            :

### Home/templates:
- base.html
    - Base dos templates html

```html
{% load static %}

<!DOCTYPE html>
<!--BASE DE TODOS OS TEMPLATES 18/10/2024-->
<html lang="pt-br">
  <head>
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style_base.css' %}">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
    {% block content %}
    {% endblock %}

    
      <div class="div-footer">
        <footer id="footer">
          <!--
          <p>© 2024 Direitos Reservados Softex</p>
          -->
          
        </footer>
      </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
```
- cadastro.html
    - Responsável pelo cadastro
- home.html
    - página inicial
- login.html
    - Responsável pelo login

### portal_do_paciente/templates
- agendamentos.html
    - Responsável pelo agendamento da consulta
- cadastrar_medicos.html
    - Apenas funcionários têm esta opção, adicinar médicos ao banco de dados
- gerenciar_pacientes.html
    - Apenas funcionários têm esta opção, cadastrar, alterar ou deletar um paciente
- portal_do_paciente.html
    - Menu contendo a vizualização de consultas, medicos, disponíveis e consultas marcadas
- remover_paciente.html
    - Responsável pela remoção do paciente
- editar_paciente
    - Responsável pela edição do paciente


### Arquivos estáticos

- Na pasta static estão contidos todos os materias usado bem como os códigos css aplicados aos templates, 
para carregar arquivos estáticos é necessário utilizar está tag:

- carregar arquivos estáticos
```html
{% load static %}
```
- Adicionar ao html, exemplo em portal_do_paciente/templates/portal_do_paciente.html
```html
<link rel="stylesheet" href="{% static 'css/style_portal_do_paciente.css' %}">
```
```
python manage.py collectstatic
```
# deploydjango
