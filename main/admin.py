from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')


class UserPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('time_create',)


class MyUserAdmin(UserAdmin):
    model = User
    list_display = (
        'id', 'username', 'first_name', 'email', 'is_staff',
        'is_active')  # Contain only fields in your `custom-user-model`
    list_filter = ('is_staff',
                   'is_active')  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    ordering = ('-is_staff', 'is_active')
    search_fields = ('username', 'id')  # Contain only fields in your `custom-user-model` intended for searching
    list_editable = ('is_active',)


admin.site.register(User, MyUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserPost, UserPostAdmin)
