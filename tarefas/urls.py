from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TarefaViewSet

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.lista_tarefas, name='lista_tarefas'),
    path('nova/', views.criar_tarefa, name='criar_tarefa'),
    path('concluir/<int:id>/', views.concluir_tarefa, name='concluir_tarefa'),
    path('excluir/<int:id>/', views.excluir_tarefa, name='excluir_tarefa'),
]

router = DefaultRouter()
router.register(r'api/tarefas', TarefaViewSet, basename='tarefa')

urlpatterns += router.urls