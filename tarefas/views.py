from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CriarUsuarioForm
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from rest_framework import viewsets
from .models import Tarefa
from .serializers import TarefaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Tarefa
from .serializers import TarefaSerializer




def registro_view(request):
    if request.method == 'POST':
        form = CriarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')
    else:
        form = CriarUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('lista_tarefas')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def lista_tarefas(request):
    tarefas = Tarefa.objects.filter(usuario=request.user)
    return render(request, 'lista_tarefas.html', {'tarefas': tarefas})

@login_required(login_url='login')
def criar_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        Tarefa.objects.create(
            titulo=titulo,
            descricao=descricao,
            usuario=request.user
        )
        return redirect('lista_tarefas')
    return render(request, 'criar_tarefa.html')

@login_required(login_url='login')
def concluir_tarefa(request, id):
    tarefa = Tarefa.objects.get(id=id, usuario=request.user)
    tarefa.concluida = True
    tarefa.save()
    return redirect('lista_tarefas')

@login_required(login_url='login')
def excluir_tarefa(request, id):
    tarefa = Tarefa.objects.get(id=id, usuario=request.user)
    tarefa.delete()
    return redirect('lista_tarefas')

class TarefaViewSet(viewsets.ModelViewSet):
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tarefa.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Tarefa.objects.filter(usuario=user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)