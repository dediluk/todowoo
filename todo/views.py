from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def signupUser(request):
    if request.method == "GET":
        return render(request, 'todo/signupUser.html', {'form': UserCreationForm})
    else:
        # User.objects.create_user()
        pass
