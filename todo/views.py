from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


def home(request):
    if request.user.is_anonymous:
        return render(request, 'todo/home.html')
    else:
        return redirect ('currentToDo')


def signupUser(request):
    if request.method == "GET":
        return render(request, 'todo/signupUser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentToDo')
            except IntegrityError:
                return render(request, 'todo/signupUser.html',
                              {'form': UserCreationForm, 'error':
                                  "Данное имя уже используется. Пожалуйста, попробуйте другое"})
        else:
            return render(request, 'todo/signupUser.html', {'form': UserCreationForm, 'error': "Пароли не совпадают"})


def loginTestUser(request):
    user = authenticate(request, username='Gatsby', password='Daisy321')
    login(request, user)
    return redirect('currentToDo')


def loginUser(request):
    if request.method == "GET":
        return render(request, 'todo/loginUser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginUser.html',
                          {'form': AuthenticationForm, 'error':
                              "Неверно введен логин и/или пароль"})
        else:
            login(request, user)
            return redirect('currentToDo')


@login_required
def currentToDo(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/currentToDo.html', {'todos': todos, 'current': 'active'})


@login_required
def logoutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


@login_required
def create(request):
    if request.method == "GET":
        return render(request, 'todo/create.html', {'form': TodoForm, 'create': 'active'})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
        except ValueError:
            return render(request, 'todo/create.html',
                          {'form': TodoForm, 'error': 'Неверно введены данные. Попробуйте ещё раз', 'create': 'active'})
        return redirect('currentToDo')


@login_required
def viewTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        print('=================================')
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            print('=================================')
            return redirect('currentToDo')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Неверные данные'})


@login_required
def completeTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currentToDo')
    else:
        return redirect('currentToDo')

@login_required
def uncompleteTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.dateCompleted = None
        todo.save()
        return redirect('currentToDo')
    else:
        return redirect('currentToDo')


@login_required
def deleteTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currentToDo')
    else:
        return redirect('currentToDo')


@login_required
def completedTodo(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/currentToDo.html', {'todos': todos, 'completed': 'active'})
