from django.contrib.auth.models import AbstractUser
from django.db import models
import requests


class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        'User', related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        'User', related_name='to_user', on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['time_create', 'title']


class UserPost(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст поста')
    user_id = models.IntegerField(null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Посты пользователей'
        ordering = ['time_create', 'title']


class Category(models.Model):  # чтобы создать категорию - Category.objects.create("Имя категории")
    # чтобы обновить у всех объектов категорию- main.objects.all().update(cat_id = 1)
    # https://www.youtube.com/watch?v=tzl1uklqM20&list=PLA0M1Bcd0w8xO_39zZll2u1lz_Q-Mwn1F&index=9
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
