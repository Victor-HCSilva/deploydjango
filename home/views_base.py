from abc import ABC, abstractmethod
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import logout
from django.utils import timezone

class BaseView(ABC):
    """Classe abstrata base para as views, fornecendo funcionalidades comuns."""

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.context = {}


    @abstractmethod
    def get_context_data(self):
        """Método abstrato para obter os dados de contexto."""
        pass

    @abstractmethod
    def render_view(self, template_name):
         """Método abstrato para renderizar a view."""
         pass
    
    def handle_search(self, queryset, search_term, filter_field):
      if search_term:
            queryset = queryset.filter(
                Q(**{f'{filter_field}__icontains':search_term})
        )
      return queryset

    def handle_pagination(self, queryset, items_per_page):
      paginator = Paginator(queryset, items_per_page)
      page = self.request.GET.get('page')
      try:
        objects = paginator.page(page)
      except PageNotAnInteger:
        objects = paginator.page(1)
      except EmptyPage:
        objects = paginator.page(paginator.num_pages)
      return objects

class LoginRequiredView(BaseView):
    """Classe base para views que exigem login."""

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.user_id = self.kwargs.get('id') # Pega o ID da URL

    def check_user_authentication(self):
       """Verifica se o usuário está autenticado e se o ID na URL coincide com o ID do usuário."""
       if self.request.user.id != int(self.user_id):
         return redirect('login')

    def handle_view(self, template_name):
        self.check_user_authentication()
        self.get_context_data()
        return self.render_view(template_name)

class FormHandlerView(BaseView):
   """Classe base para views que gerenciam formulários."""
   def __init__(self, request, form_class, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.form_class = form_class
        self.form = None
   
   def create_form(self,data=None, instance=None):
      self.form = self.form_class(data,instance=instance)
   
   def validate_form(self):
      if self.form.is_valid():
          return self.form.save()
      else:
          return None