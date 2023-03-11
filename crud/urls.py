from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("Singup/", views.Singup, name="singup"),
    path("Tasks/", views.Tareas, name="tasks"),
    path("Tasks/completadas", views.TareasCompletadas, name="tasks_completadas"),
    path("Tasks/<int:task_id>/", views.ObtenerTareas, name="tasks_details"),
    path("Tasks/<int:task_id>/complete", views.CompletarTarea, name="completed_task"),
    path("Tasks/<int:task_id>/delete", views.EliminarTarea, name="eliminar_task"),
    path("Logout/", views.singout, name="logout"),
    path("Singin/", views.singin, name="singin"),
    path("Tasks/Create", views.CrearTarea, name='creartarea')
]
