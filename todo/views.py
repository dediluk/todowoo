from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


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


def currentToDo(request):
    return render(request, 'todo/currentToDo.html')
