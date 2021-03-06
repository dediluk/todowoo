"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # authy
    path('signup/', views.signupUser, name='signupUser'),
    path('login/', views.loginUser, name='loginUser'),
    path('logintestuser/', views.loginTestUser, name='loginTestUser'),
    path('logout/', views.logoutUser, name='logoutUser'),

    # todos
    path('currenttodo/', views.currentToDo, name='currentToDo'),
    path('completedtodo/', views.completedTodo, name='completedTodo'),
    path('create/', views.create, name='create'),
    path('viewtodo/<int:todo_pk>', views.viewTodo, name='viewTodo'),
    path('viewtodo/<int:todo_pk>/complete', views.completeTodo, name='completeTodo'),
    path('viewtodo/<int:todo_pk>/uncomplete', views.uncompleteTodo, name='uncompleteTodo'),
    path('viewtodo/<int:todo_pk>/delete', views.deleteTodo, name='deleteTodo'),
    path('', views.home, name='home'),
]
