from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaksForm
from .models import Tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def Singup(request):
    if request.method == "GET":
        return render(request, "Singup.html")
    else:
        if request.POST["password"] == request.POST["2password"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["name"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "Singup.html", {"error": "El usuario ya existe"})
        else:
            return render(
                request, "Singup.html", {"error": "La Constraseña es distinta"}
            )


def Home(request):
    return render(request, "Home.html")

@login_required
def Tareas(request):
    tasks= Tasks.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {'tasks': tasks})
@login_required
def ObtenerTareas(request,task_id):
    if request.method == 'GET':      
        tasks= get_object_or_404(Tasks, pk=task_id, user=request.user)
        form = TaksForm(instance=tasks)
        return render(request, "task_detail.html", {'tasks': tasks, 'form':form})
    else:
        try:
            tasks= get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = TaksForm(request.POST, instance=tasks)
            form.save()
            return redirect('tasks')
        except ValueError:
            tasks= get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = TaksForm(request.POST, instance=tasks)
            error = 'Ha ocurrido un error inserte datos nuevamente'
            return render(request, "task_detail.html", {'tasks': tasks, 'form':form, 'error':error})
@login_required
def CompletarTarea(request, task_id):
        task = get_object_or_404(Tasks, pk=task_id, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def EliminarTarea(request, task_id):
        task = get_object_or_404(Tasks, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')
@login_required
def TareasCompletadas(request):
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, "tasks.html", {'tasks': tasks})
@login_required
def CrearTarea(request):
    if request.method == "GET":
        return render(request, "crear_tarea.html", {"form": TaksForm})
    else:
        try:
            formulario = TaksForm(request.POST)
            nueva_tarea = formulario.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "crear_tarea.html",
                {"form": TaksForm, "error": "Ha Ocurrido un Error"},
            )

@login_required
def singout(request):
    logout(request)
    return redirect("home")


def singin(request):
    if request.method == "GET":
        return render(request, "Singin.html")
    else:
        autenticacion = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if autenticacion == None:
            return render(
                request,
                "Singin.html",
                {"error": "El usuario o contraseña es incorrecto"},
            )
        else:
            login(request, autenticacion)
            return redirect("home")
