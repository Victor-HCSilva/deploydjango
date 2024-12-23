
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AgendamentoConsulta
from pacientes.models import Paciente
from medicos.models import Medico
from django.contrib.auth.decorators import login_required
from datetime import time

@login_required
def agendar_consulta(request, id):
    
    if request.user.id != int(id):  
        return redirect('login')  
    try:
        paciente = Paciente.objects.get(id=id)
    except Paciente.DoesNotExist:
        return redirect('cadastro')

    if request.method == 'POST':
        data_consulta = request.POST.get('data_consulta')  
        hora_consulta = request.POST.get('hora_consulta')
        id_medico = request.POST.get('id_medico')

        if not data_consulta or not hora_consulta or not id_medico:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('agendar_consulta', id=id)

        # Buscar o médico selecionado
        try:
            medico = Medico.objects.get(id=id_medico)
        except Medico.DoesNotExist:
            messages.error(request, "Médico inválido.")
            return redirect('agendar_consulta', id=id)

        # Verificar se o médico já tem uma consulta naquele horário
        if AgendamentoConsulta.objects.filter(medico=medico, data=data_consulta, hora=hora_consulta).exists():
            messages.error(request, f"O médico {medico.nome} já tem uma consulta agendada para este horário.")
            return redirect('agendar_consulta', id=id)

        # Criar o agendamento
        AgendamentoConsulta.objects.create( 
            paciente=paciente,
            medico=medico,
            data=data_consulta,  # Mantém o formato original
            hora=hora_consulta
        )

        messages.success(request, "Consulta agendada com sucesso!")
        return redirect('portal_do_paciente', id=id) # Passa o id do paciente para a rota

    # Carregar a página de agendamento
    medicos = Medico.objects.all()  # Listar médicos para o formulário
    
    HORARIOS_MAP = {
    "1": time(8, 0),    # 08:00 às 09:00
    "2": time(9, 0),    # 09:00 às 10:00
    "3": time(10, 0),   # 10:00 às 11:00
    "4": time(11, 0),   # 11:00 às 12:00
    "5": time(12, 0),   # 12:00 às 13:00
    "6": time(13, 0),   # 13:00 às 14:00
}

    context = {
        'paciente': paciente,
        'medicos': medicos,
        'horarios': HORARIOS_MAP,
    }

    return render(request, 'agendamento.html', context)

###No app portal do paciente

