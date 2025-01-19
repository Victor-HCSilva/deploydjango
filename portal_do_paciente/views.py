from pacientes.models import Paciente
from pacientes.forms import PacienteForm
from medicos.models import Medico, Especialidade
from medicos.forms import MedicoForm
from agendamentos.models import AgendamentoConsulta
from django.contrib.auth.decorators import login_required
from .views_base import (
    BaseView, LoginRequiredView, datetime, render, messages, redirect, get_object_or_404,
    FormHandlerView, timezone, logout,
)


class PortalDoPacienteView(LoginRequiredView):
    def get_context_data(self):
        DATA = datetime.now()
        paciente = Paciente.objects.get(id=int(self.user_id))
        search_term = self.request.GET.get('search', '')
        specialty_term = self.request.GET.get('specialty', '')

        medicos_query = Medico.objects.all()

        medicos_query = self.handle_search(medicos_query, search_term, "nome")
        medicos_query = self.handle_search(medicos_query, specialty_term, "especialidade__nome")

        medicos = self.handle_pagination(medicos_query, 5)

        agendamentos = AgendamentoConsulta.objects.all()

        try:
            FIRST_NAME = paciente.nome.split()[0].title()
        except:
            if paciente.is_staff == True:
                FIRST_NAME = 'ADM'
            else:
                FIRST_NAME = "Not found"

        specialties = Especialidade.objects.all()
        IS_ADMIN = False
        self.context = {
            'paciente': paciente,
            'data': DATA,
            'admin': IS_ADMIN,
            'name': FIRST_NAME,
            'medicos': medicos,
            'agendamentos': agendamentos,
            'search_term': search_term,
            'specialty_term': specialty_term,
            'specialties': specialties,
        }

    def render_view(self, template_name):
        return render(self.request, template_name, self.context)


@login_required
def portal_do_paciente(request, id):
    view = PortalDoPacienteView(request, id=id)
    return view.handle_view('portal_do_paciente.html')


class AgendarConsultaView(LoginRequiredView):
    def get_context_data(self):

        try:
            paciente = Paciente.objects.get(id=self.user_id)
        except Paciente.DoesNotExist:
            return redirect('cadastro')

        if self.request.method == 'POST':
            data_consulta = self.request.POST.get('data_consulta')
            hora_consulta = self.request.POST.get('hora_consulta')
            id_medico = self.request.POST.get('id_medico')

            if not data_consulta or not hora_consulta or not id_medico:
                messages.error(self.request, "Todos os campos são obrigatórios.")
                return redirect('agendar_consulta', id=self.user_id)
            try:
                medico = Medico.objects.get(id=id_medico)
            except Medico.DoesNotExist:
                messages.error(self.request, "Médico inválido.")
                return redirect('agendar_consulta', id=self.user_id)

            try:
                hora_consulta = datetime.strptime(hora_consulta, '%H:%M').time()
            except ValueError:
                messages.error(self.request, "Formato de horário inválido.")
                return redirect('agendar_consulta', id=self.user_id)

            if AgendamentoConsulta.objects.filter(medico=medico, data=data_consulta, hora=hora_consulta).exists():
                messages.error(self.request, f"O médico {medico.nome} já tem uma consulta agendada para este horário.")
                return redirect('agendar_consulta', id=self.user_id)

            AgendamentoConsulta.objects.create(
                paciente=paciente,
                medico=medico,
                data=data_consulta,
                hora=hora_consulta
            )

            messages.success(self.request, "Consulta agendada com sucesso!")
            return redirect('portal_do_paciente', id=self.user_id)

        medicos = Medico.objects.all()
        HORARIOS_DICT = {
            "08:00": "08:00 às 09:00",
            "09:00": "09:00 às 10:00",
            "10:00": "10:00 às 11:00",
            "11:00": "11:00 às 12:00",
            "12:00": "12:00 às 13:00",
            "13:00": "13:00 às 14:00"
        }
        self.context = {
            'paciente': paciente,
            'medicos': medicos,
            'horarios': HORARIOS_DICT
        }
        hoje = timezone.now().date()
        consultas_antigas = AgendamentoConsulta.objects.filter(data__lt=hoje)
        consultas_antigas.delete()

    def render_view(self, template_name):
        return render(self.request, template_name, self.context)


@login_required
def agendar_consulta(request, id):
    view = AgendarConsultaView(request, id=id)
    return view.handle_view('agendamento.html')


def logout_view(request):
    logout(request)
    return redirect('login')


class CadastroDeMedicosView(FormHandlerView):
    def get_context_data(self):
        paciente = get_object_or_404(Paciente, id=self.user_id)
        if self.request.method == 'POST':
            self.create_form(data=self.request.POST)
            medico = self.validate_form()
            if medico:
                medico.password = self.form.cleaned_data['password']  # Seta a senha
                medico.save()  # Salva o medico no banco de dados
                messages.success(self.request, "Médico cadastrado com sucesso!")
                return redirect('portal_do_paciente', id=self.user_id)
            else:
                messages.error(self.request, "Por favor, corrija os erros no formulário.")
        else:
            self.create_form()
        self.context = {
            'paciente': paciente,
            'form': self.form
        }

    def render_view(self, template_name):
        return render(self.request, template_name, self.context)


@login_required
def cadastro_de_medicos(request, id):
    view = CadastroDeMedicosView(request, MedicoForm, id=id)
    return view.handle_view('cadastrar_medicos.html')


class GestaoDePacientesView(FormHandlerView):
    def get_context_data(self):
        all_pacientes = Paciente.objects.all()
        medicos = Medico.objects.all()
        all_agendamentos = AgendamentoConsulta.objects.all()  # Obtém todos os agendamentos
        adm = get_object_or_404(Paciente, id=self.user_id)

        # Filtros para pacientes
        search_query_pacientes = self.request.GET.get('search_pacientes', '')
        cpf_filter_pacientes = self.request.GET.get('cpf_search_pacientes', '')
        all_pacientes = self.handle_search(all_pacientes, search_query_pacientes, "nome")
        all_pacientes = self.handle_search(all_pacientes, cpf_filter_pacientes, "cpf")
        pacientes = self.handle_pagination(all_pacientes, 5)


        # Filtros para agendamentos
        medico_cpf_filter = self.request.GET.get('medico_cpf_search', '')
        paciente_cpf_filter = self.request.GET.get('paciente_cpf_search', '')

        if medico_cpf_filter:
            all_agendamentos = all_agendamentos.filter(medico__cpf__icontains=medico_cpf_filter)
        if paciente_cpf_filter:
            all_agendamentos = all_agendamentos.filter(paciente__cpf__icontains=paciente_cpf_filter)

        agendamentos = self.handle_pagination(all_agendamentos, 5)

        if self.request.method == 'POST':
            self.create_form(data=self.request.POST)
            paciente = self.validate_form()

            if paciente:
                paciente.set_password(self.form.cleaned_data['password'])
                paciente.data_de_nascimento = self.form.cleaned_data['data_de_nascimento']
                paciente.is_staff = False
                paciente.is_superuser = False
                paciente.is_active = True
                paciente.save()
                messages.success(self.request, 'Paciente cadastrado com sucesso!')

            else:
                messages.error(self.request, 'ocorreu um erro no formulário!')

            self.context = {
                'form': self.form,
                'pacientes': pacientes,
                'adm': adm,
                'medicos': medicos,
                'agendamentos': agendamentos,
                'search_query_pacientes': search_query_pacientes,
                'cpf_filter_pacientes': cpf_filter_pacientes,
                'medico_cpf_filter': medico_cpf_filter,
                'paciente_cpf_filter': paciente_cpf_filter,
            }

            return redirect('portal_do_paciente', id=self.user_id)

        elif self.request.method == 'GET':
            self.create_form(data=self.request.POST)
            self.context = {
                'form': self.form,
                'pacientes': pacientes,
                'adm': adm,
                'medicos': medicos,
                'agendamentos': agendamentos,
                'search_query_pacientes': search_query_pacientes,
                'cpf_filter_pacientes': cpf_filter_pacientes,
                'medico_cpf_filter': medico_cpf_filter,
                'paciente_cpf_filter': paciente_cpf_filter,
            }

    def render_view(self, template_name):
        return render(self.request, template_name, self.context)


@login_required
def gestao_de_pacientes(request, id):
    view = GestaoDePacientesView(request, PacienteForm, id=id)
    return view.handle_view('gerenciar_pacientes.html')


class EditarPacienteView(FormHandlerView):
    def get_context_data(self):
        try:
            paciente = get_object_or_404(Paciente, id=self.kwargs.get('id_paciente'))  # Usa get_object_or_404 para lidar com Paciente inexistente
            adm = get_object_or_404(Paciente, id=self.user_id)  # Usa get_object_or_404 para lidar com Paciente inexistente
        except:
            messages.error(self.request, 'Ocorreu um erro ao tentar realizar operação.')
            return redirect('cadastro')

        if self.request.method == 'POST':
            self.create_form(data=self.request.POST, instance=paciente)
            paciente = self.validate_form()
            if paciente:
                paciente.set_password(self.form.cleaned_data['password'])
                paciente.data_de_nascimento = self.form.cleaned_data['data_de_nascimento']
                paciente.is_staff = False
                paciente.is_superuser = False
                paciente.is_active = True
                paciente.save()
                return redirect('portal_do_paciente', id=self.user_id)
            else:
                self.context = {'form': self.form, 'paciente': paciente,
                                'erro': 'Formulário inválido. Verifique os campos.'}
                return self.render_view('editar_paciente.html')  # Renderiza a mesma página com os erros
        else:
            self.create_form(instance=paciente)

        self.context = {
            'form': self.form,
            'paciente': paciente,
            'ADM_ID': adm.id,
        }

    def render_view(self, template_name):
        return render(self.request, template_name, self.context)


@login_required
def editar_paciente(request, id_paciente, id_adm):
    view = EditarPacienteView(request, PacienteForm, id=id_adm, id_paciente=id_paciente)
    return view.handle_view('editar_paciente.html')


class RemoverPacienteView(LoginRequiredView):
    def get_context_data(self):
        paciente = get_object_or_404(Paciente, id=self.kwargs.get('id'))
        adm = get_object_or_404(Paciente, id=self.user_id)
        if self.request.method == "POST":
            paciente.delete()
            messages.success(self.request, "Consulta agendada com sucesso!")
            return redirect('portal_do_paciente', id=self.user_id)
        else:
            self.context = {'paciente': paciente,
                            'erro': 'Formulário inválido. Verifique os campos.',
                            'adm': adm,
                            }

    def render_view(self, template_name):
        return render(self.request, template_name, self.context)


@login_required
def remover_paciente(request, id, id_adm):
    view = RemoverPacienteView(request, id=id_adm, id_paciente=id)
    return view.handle_view('remover_paciente.html')