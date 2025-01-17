from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from pacientes.forms import PacienteForm
from pacientes.models import Paciente

def remover_formatacao_cpf(cpf:str = '123.456.789-10'):
  """
  Remove pontos e traços de um CPF formatado.

  Args:
      cpf: O CPF formatado (ex: '123.456.789-00').

  Returns:
      O CPF sem formatação (ex: '12345678900').
  """
  return cpf.replace('.', '').replace('-', '')



def home(request):
    #paciente = Paciente.objects.get(id=int(id))  # Obtenha o paciente

    context ={
     #   'paciente':paciente,#Chama-se com a chave, não o valor
    }
    return render(request, 'home.html')

def login_(request):
    
    """
    View para efetuar o login de um paciente.
    """
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')

        print(password)
        print(cpf)
        # Autentica o usuário usando CPF (definido como username no modelo) e senha
        user = authenticate(username=cpf, password=str(password)) 
        print(user)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('portal_do_paciente', id=user.id)  # Redireciona para o portal do paciente
        else:
            messages.error(request, 'CPF ou senha inválidos!')
            return render(request, 'login.html')

    return render(request, 'login.html')

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
            paciente.nome = paciente.nome.title()
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
    

def teste(request):
    return render(request, 'teste.html')

def view(request):
    return render(request, 'administracao.html')