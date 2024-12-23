from pacientes.models import Paciente
from pacientes.forms import PacienteForm
from medicos.models import Medico
from medicos.forms import MedicoForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime,time
from django.contrib import messages
from django.contrib.auth import logout,login
from agendamentos.models import AgendamentoConsulta

@login_required
def portal_do_paciente(request, id):
    DATA = datetime.now()
    
    # Verifique se o usuário tem permissão para acessar os dados do paciente
    if request.user.id != int(id):  # Converta o id para inteiro e compare
        return redirect('login')  # Redirecione para a página de login
    
    paciente = Paciente.objects.get(id=int(id))  # Obtenha o paciente
    medicos = Medico.objects.all()
    agendamentos = AgendamentoConsulta.objects.all()

    try:
        FIRST_NAME =  paciente.nome.split()[0].title()
    except:
        FIRST_NAME =  "Not found"
    
    #A fazer ...
    IS_ADMIN = False    

    #Variaves passadas ao template
    context = {
        'paciente': paciente,  # Adicione o objeto paciente ao contexto
        'data':DATA, # Data
        'admin': IS_ADMIN,
        'name': FIRST_NAME,
        'medicos':medicos,
        'agendamentos':agendamentos,
    }
    return render(request, 'portal_do_paciente.html', context)

from datetime import datetime

@login_required
def agendar_consulta(request, id):
    try:
        paciente = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return redirect('cadastro')

    if request.user.id != int(id):
        return redirect('login')  
    
    if request.method == 'POST':
        data_consulta = request.POST.get('data_consulta')  
        hora_consulta = request.POST.get('hora_consulta')
        id_medico = request.POST.get('id_medico')

        if not data_consulta or not hora_consulta or not id_medico:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('agendar_consulta', id=id)

        try:
            medico = Medico.objects.get(id=id_medico)
        except Medico.DoesNotExist:
            messages.error(request, "Médico inválido.")
            return redirect('agendar_consulta', id=id)

        # Conversão de string para datetime.time
        try:
            hora_consulta = datetime.strptime(hora_consulta, '%H:%M').time()
        except ValueError:
            messages.error(request, "Formato de horário inválido.")
            return redirect('agendar_consulta', id=id)

        if AgendamentoConsulta.objects.filter(medico=medico, data=data_consulta, hora=hora_consulta).exists():
            messages.error(request, f"O médico {medico.nome} já tem uma consulta agendada para este horário.")
            return redirect('agendar_consulta', id=id)

        AgendamentoConsulta.objects.create( 
            paciente=paciente,
            medico=medico,
            data=data_consulta,
            hora=hora_consulta
        )

        messages.success(request, "Consulta agendada com sucesso!")
        return redirect('portal_do_paciente', id=id)

    medicos = Medico.objects.all()
    HORARIOS_DICT = {
        "08:00": "08:00 às 09:00", 
        "09:00": "09:00 às 10:00", 
        "10:00": "10:00 às 11:00", 
        "11:00": "11:00 às 12:00", 
        "12:00": "12:00 às 13:00", 
        "13:00": "13:00 às 14:00"
    }
    context = {
        'paciente': paciente,
        'medicos': medicos,
        'horarios': HORARIOS_DICT
    }
    from django.utils import timezone
    #deleção de consultas
    hoje = timezone.now().date()
    consultas_antigas = AgendamentoConsulta.objects.filter(data__lt=hoje)
    consultas_antigas.delete()


    return render(request, 'agendamento.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirecione para a página de login

@login_required
def cadastro_de_medicos(request, id):
    paciente = get_object_or_404(Paciente, id=id)  # Use get_object_or_404 para lidar com 404

    if request.user.id != int(id):  # Verifica se o usuário logado é o paciente correto
        return redirect('login')

    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            medico = form.save(commit=False)  # Salva o medico mas não salva ainda no banco de dados
            medico.password = form.cleaned_data['password'] #Seta a senha
            medico.save()  # Salva o medico no banco de dados
            messages.success(request, "Médico cadastrado com sucesso!")
            return redirect('portal_do_paciente', id=id)
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = MedicoForm()

    context = {'paciente': paciente, 'form': form}
    return render(request, 'cadastrar_medicos.html', context)




@login_required
def gestao_de_pacientes(request, id):
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    agendamentos = AgendamentoConsulta.objects.all()

    try:
        paciente = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return redirect('cadastro')
    
    if request.user.id != int(id):
        return redirect('login')
    
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
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
            messages.success(request, 'Paciente cadastrado com sucesso!')

        else:
            messages.error(request, 'ocorreu um erro no formulário!')

        context = {
            'form': form,  # Certifique-se que 'form' está sempre no contexto
            'pacientes': pacientes,
            'paciente': paciente,
            'medicos':medicos,
            'agendamentos':agendamentos,
        }

        return redirect('portal_do_paciente', id=id)
    
    elif request.method == 'GET':
        form = PacienteForm(request.POST)
        context = {
            'form': form,  # Certifique-se que 'form' está sempre no contexto
            'pacientes': pacientes,
            'paciente': paciente,
            'medicos':medicos,
            'agendamentos':agendamentos,
        }
        return render(request, 'gerenciar_pacientes.html',context)

@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id) # Usa get_object_or_404 para lidar com Paciente inexistente
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():

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
            return redirect('portal_do_paciente',id=id) # Redireciona para o portal do paciente
        else:
            # Mensagem de erro para formulário inválido
            contexto = {'form': form, 'paciente': paciente, 'erro': 'Formulário inválido. Verifique os campos.'}
            return render(request, 'editar_paciente.html', contexto) # Renderiza a mesma página com os erros
    else:
        form = PacienteForm(instance=paciente)

    context = {'form': form, 'paciente': paciente}
    return render(request, 'editar_paciente.html', context)

def remover_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id) 
    if request.method=="POST":
        paciente.delete() 
        return redirect('portal_do_paciente', id=id)
    else:
            # Mensagem de erro para formulário inválido
        contexto = {'paciente': paciente, 'erro': 'Formulário inválido. Verifique os campos.'}
        return render(request, 'remover_paciente.html', contexto) # Renderiza a mesma página com os erros


