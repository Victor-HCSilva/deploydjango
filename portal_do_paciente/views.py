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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def portal_do_paciente(request, id):
    DATA = datetime.now()

    # Verifique se o usuário tem permissão para acessar os dados do paciente
    if request.user.id != int(id):  # Converta o id para inteiro e compare
        return redirect('login')  # Redirecione para a página de login

    paciente = Paciente.objects.get(id=int(id))  # Obtenha o paciente
    medicos_list = Medico.objects.all()  # Obtém todos os médicos

    # Configuração da paginação
    paginator = Paginator(medicos_list, 5)  # Mostra 5 médicos por página
    page = request.GET.get('page')  # Obtém o número da página da URL

    try:
        medicos = paginator.page(page) # Obtem a pagina desejada
    except PageNotAnInteger:
        medicos = paginator.page(1) # Se não for inteiro, exibe a primeira
    except EmptyPage:
        medicos = paginator.page(paginator.num_pages) # Se for maior que o limite, exibe a ultima pagina

    agendamentos = AgendamentoConsulta.objects.all()

    try:
        FIRST_NAME =  paciente.nome.split()[0].title()
    except:
        if paciente.is_staff == True:
            FIRST_NAME = 'ADM'
        else:
            FIRST_NAME =  "Not found"

    #A fazer ...
    IS_ADMIN = False

    #Variaves passadas ao template
    context = {
        'paciente': paciente,  # Adicione o objeto paciente ao contexto
        'data':DATA, # Data
        'admin': IS_ADMIN,
        'name': FIRST_NAME,
        'medicos':medicos,  # Agora, 'medicos' é uma página do paginator
        'agendamentos':agendamentos,
    }
    return render(request, 'portal_do_paciente.html', context)


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
        adm = Paciente.objects.get(id=id)
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
            'adm': adm,
            'medicos':medicos,
            'agendamentos':agendamentos,
        }

        return redirect('portal_do_paciente', id=id)
    
    elif request.method == 'GET':
        form = PacienteForm(request.POST)
        context = {
            'form': form,  # Certifique-se que 'form' está sempre no contexto
            'pacientes': pacientes,
            'adm': adm,
            'medicos':medicos,
            'agendamentos':agendamentos,
        }
        return render(request, 'gerenciar_pacientes.html',context)

@login_required
def editar_paciente(request, id_paciente, id_adm):
    try:
        paciente = get_object_or_404(Paciente, id=id_paciente) # Usa get_object_or_404 para lidar com Paciente inexistente
        adm = get_object_or_404(Paciente, id=id_adm) # Usa get_object_or_404 para lidar com Paciente inexistente
    except:
        messages.error(request, 'Ocorreu um erro ao tentar realizar operação.')
        return redirect('cadastro')
    
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
            return redirect('portal_do_paciente',id=id_adm) # Redireciona para o portal do paciente
        else:
            # Mensagem de erro para formulário inválido
            contexto = {'form': form, 'paciente': paciente, 'erro': 'Formulário inválido. Verifique os campos.'}
            return render(request, 'editar_paciente.html', contexto) # Renderiza a mesma página com os erros
    else:
        form = PacienteForm(instance=paciente)

    context = {
            'form': form,
            'paciente': paciente,
            'ADM_ID': adm.id,
            }
    return render(request, 'editar_paciente.html', context)

def remover_paciente(request, id, id_adm):
    paciente = get_object_or_404(Paciente, id=id) 
    adm = get_object_or_404(Paciente, id=id_adm)

    if request.method=="POST":
        paciente.delete() 
        messages.success(request, "Consulta agendada com sucesso!")
        return redirect('portal_do_paciente', id=id_adm)
    else:
            # Mensagem de erro para formulário inválido
        context = {'paciente': paciente,
                     'erro': 'Formulário inválido. Verifique os campos.',
                     'adm': adm,
                     }
        return render(request, 'remover_paciente.html',context
                      ) # Renderiza a mesma página com os erros


