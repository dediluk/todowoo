from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


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


def currentToDo(request):
    todos = Todo.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/currentToDo.html', {'todos': todos})


def logoutUser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def create(request):
    if request.method == "GET":
        return render(request, 'todo/create.html', {'form': TodoForm})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
        except ValueError:
            return render(request, 'todo/create.html',
                          {'form': TodoForm, 'error': 'Неверно введены данные. Попробуйте ещё раз'})
        return redirect('currentToDo')
