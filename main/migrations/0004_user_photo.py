# Generated by Django 4.0.3 on 2022-04-16 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_friendrequest_from_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='usersphoto'),
        ),
    ]