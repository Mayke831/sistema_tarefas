from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'concluida', 'data_criacao')
    list_filter = ('concluida', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'usuario__username')