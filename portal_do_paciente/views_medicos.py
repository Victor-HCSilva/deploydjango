from django.contrib import messages
from medicos.models import Medico
from medicos.forms import MedicoForm
from pacientes.models import Paciente
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


@login_required
def gestao_de_medicos(request, id):

    if request.user.id != int(id):
        return redirect('login')
    
    medicos = Medico.objects.all()
    search_term = request.GET.get('search_cpf','') #Obtém o parametro 'search_cpf' via GET

    if search_term:
      medicos = medicos.filter(cpf__icontains=search_term) #Filtrar por CPF, icontains para pesquisa não case-sensitive

    #Configuração da paginação
    page = request.GET.get('page', 1)
    paginator = Paginator(medicos, 5) # Mostra 5 médicos por página
    try:
        medicos = paginator.page(page)
    except PageNotAnInteger:
        medicos = paginator.page(1) # Se a página não for um inteiro, mostra a primeira página
    except EmptyPage:
        medicos = paginator.page(paginator.num_pages)  # Se a página estiver vazia, mostra a última página


    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portal_do_paciente', id=id)  # Redireciona para a mesma página após salvar
    else:
        form = MedicoForm()

    context = {
        'medicos': medicos,
        'form': form,
        'search_term': search_term,
        'id':id,
    }
    return render(request, 'gestao_de_medicos.html', context)

@login_required
def editar_medico(request, id_medico, id_adm):
    try:
        medico = get_object_or_404(Medico, id=id_medico) 
        adm = get_object_or_404(Paciente, id=id_adm) 
    except:
        messages.error(request, 'Ocorreu um erro ao tentar realizar operação.')
        return redirect('cadastro')
    
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():

            medico = form.save(commit=False)  
            medico.set_password(form.cleaned_data['password'])            
            medico.data_de_nascimento = form.cleaned_data['data_de_nascimento']
            medico.is_staff = False
            medico.is_superuser = False
            medico.is_active = True
            medico.save()

            return redirect('portal_do_paciente',id=id_adm) # Redireciona para o portal do paciente
        else:
            # Mensagem de erro para formulário inválido
            contexto = {'form': form, 'medico': medico, 'erro': 
                        'Formulário inválido. Verifique os campos.'
                        }
            
            return render(request, 'editar_medico.html', contexto) # Renderiza a mesma página com os erros
    else:
        form = MedicoForm(instance=medico)

    context = {
            'form': form,
            'medico': medico,
            'id_adm': adm.id,
            }
    return render(request, 'editar_medico.html', context)

@login_required
def remover_medico(request, id_medico, id_adm):
    medico = get_object_or_404(Medico, id=id_medico) 
    adm = get_object_or_404(Paciente, id=id_adm)

    if request.method=="POST":
        medico.delete() 
        messages.success(request, "Removido!")
        return redirect('portal_do_paciente', id=id_adm)
    else:
            # Mensagem de erro para formulário inválido
        context = {'medico': medico,
                     'erro': 'Formulário inválido. Verifique os campos.',
                     'adm': adm,
                     }
        return render(request, 'remover_medico.html',context
                      ) # Renderiza a mesma página com os erros


