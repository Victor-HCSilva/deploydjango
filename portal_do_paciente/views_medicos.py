from django.shortcuts import render, redirect
from medicos.forms import MedicoForm
from medicos.models import Medico
from django.contrib.auth.decorators import login_required

@login_required
def gestao_de_medicos(request, id):
    
    """
    View que exibe a lista de médicos e permite criar novos médicos e pesquisar por CPF.

    Args:
        request (HttpRequest): Objeto de requisição HTTP.

    Returns:
        HttpResponse: Resposta HTTP renderizando o template 'medicos/medico_list_create.html'.
    """
    medicos = Medico.objects.all()
    search_term = request.GET.get('search_cpf', '') #Obtém o parametro 'search_cpf' via GET

    if search_term:
      medicos = medicos.filter(cpf__icontains=search_term) #Filtrar por CPF, icontains para pesquisa não case-sensitive

    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portal_do_paciente',id=id)  # Redireciona para a mesma página após salvar
    else:
        form = MedicoForm()

    context = {
        'medicos': medicos,
        'form': form,
        'search_term': search_term #Passa o valor pesquisado para o template
    }
    return render(request, 'gestao_de_medicos.html', context)