from pacientes.models import Paciente
from pacientes.forms import PacienteForm
from medicos.models import Medico, Especialidade
from medicos.forms import MedicoForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime,time
from django.contrib import messages
from django.contrib.auth import logout,login
from agendamentos.models import AgendamentoConsulta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required
def portal_do_paciente(request, id):
    DATA = datetime.now()

    if request.user.id != int(id):
        return redirect('login')

    paciente = Paciente.objects.get(id=int(id))

    # Obter termos de pesquisa
    search_term = request.GET.get('search', '')
    specialty_term = request.GET.get('specialty', '')

    medicos_query = Medico.objects.all()

    # Aplicar filtro por nome
    if search_term:
        medicos_query = medicos_query.filter(
            Q(nome__icontains=search_term)
        )
    
    # Aplicar filtro por especialidade
    if specialty_term:
      medicos_query = medicos_query.filter(
            Q(especialidade__nome__icontains=specialty_term)
        )

    paginator = Paginator(medicos_query, 5)
    page = request.GET.get('page')

    try:
        medicos = paginator.page(page)
    except PageNotAnInteger:
        medicos = paginator.page(1)
    except EmptyPage:
        medicos = paginator.page(paginator.num_pages)

    agendamentos = AgendamentoConsulta.objects.all()

    try:
        FIRST_NAME =  paciente.nome.split()[0].title()
    except:
        if paciente.is_staff == True:
            FIRST_NAME = 'ADM'
        else:
            FIRST_NAME =  "Not found"
    
    specialties = Especialidade.objects.all()

    IS_ADMIN = False

    context = {
        'paciente': paciente,
        'data':DATA,
        'admin': IS_ADMIN,
        'name': FIRST_NAME,
        'medicos': medicos,
        'agendamentos':agendamentos,
        'search_term': search_term,
        'specialty_term':specialty_term,
        'specialties':specialties,
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
    """
    Exibe a lista de pacientes, aplica filtros, paginação, e gerencia o formulário de cadastro.
    """
    all_pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    all_agendamentos = AgendamentoConsulta.objects.all()  # Obtém todos os agendamentos

    try:
        adm = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return redirect('cadastro')
    
    if request.user.id != int(id):
        return redirect('login')

    search_query = request.GET.get('search') or ''
    cpf_filter = request.GET.get('cpf_search') or ''
    medico_cpf_filter = request.GET.get('medico_cpf_search') or ''
    paciente_cpf_filter = request.GET.get('paciente_cpf_search') or ''


    if search_query:
        all_pacientes = all_pacientes.filter(nome__icontains=search_query)
    
    if cpf_filter:
        all_pacientes = all_pacientes.filter(cpf__icontains=cpf_filter)

    # Paginação de pacientes
    pacientes_paginator = Paginator(all_pacientes, 5)
    pacientes_page = request.GET.get('pacientes_page')  # Use um parâmetro diferente para evitar conflito
    try:
        pacientes = pacientes_paginator.get_page(pacientes_page)
    except PageNotAnInteger:
        pacientes = pacientes_paginator.get_page(1)
    except EmptyPage:
        pacientes = pacientes_paginator.get_page(pacientes_paginator.num_pages)

    # Filtro e Paginação de agendamentos
    if medico_cpf_filter:
      all_agendamentos = all_agendamentos.filter(medico__cpf__icontains=medico_cpf_filter)

    if paciente_cpf_filter:
        all_agendamentos = all_agendamentos.filter(paciente__cpf__icontains=paciente_cpf_filter)



    agendamentos_paginator = Paginator(all_agendamentos, 5) # Define quantos agendamentos por página
    agendamentos_page = request.GET.get('agendamentos_page')  # Novo parâmetro para a página de agendamentos
    try:
        agendamentos = agendamentos_paginator.get_page(agendamentos_page)
    except PageNotAnInteger:
        agendamentos = agendamentos_paginator.get_page(1)
    except EmptyPage:
        agendamentos = agendamentos_paginator.get_page(agendamentos_paginator.num_pages)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.set_password(form.cleaned_data['password'])
            paciente.data_de_nascimento = form.cleaned_data['data_de_nascimento']
            paciente.is_staff = False
            paciente.is_superuser = False
            paciente.is_active = True        
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
        else:
            messages.error(request, 'ocorreu um erro no formulário!')
    
        context = {
            'form': form,
            'pacientes': pacientes,
            'adm': adm,
            'medicos':medicos,
            'agendamentos': agendamentos,
             'search_query': search_query,
             'cpf_filter': cpf_filter,
              'medico_cpf_filter':medico_cpf_filter,
            'paciente_cpf_filter': paciente_cpf_filter,
        }

        return redirect('portal_do_paciente', id=id)
    
    elif request.method == 'GET':
        form = PacienteForm(request.POST)
        context = {
            'form': form,
            'pacientes': pacientes,
            'adm': adm,
            'medicos':medicos,
            'agendamentos': agendamentos,
            'search_query':search_query,
            'cpf_filter': cpf_filter,
             'medico_cpf_filter':medico_cpf_filter,
            'paciente_cpf_filter': paciente_cpf_filter,
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

@login_required
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


