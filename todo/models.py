from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    description = models.TextField(verbose_name='Описание', blank=True)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    dateCompleted = models.DateTimeField(verbose_name='Дата выполнения', null=True, blank=True)
    important = models.BooleanField(verbose_name='Важно', default=False)

    # done = models.BooleanField()

    def __str__(self):
        return self.title
