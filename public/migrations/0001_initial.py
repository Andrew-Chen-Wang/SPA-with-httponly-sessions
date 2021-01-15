# Generated by Django 3.1.5 on 2021-01-15 06:45

from django.db import migrations
from django.contrib.auth.models import User

from public.utils import USERNAME, EMAIL, PASSWORD


def create_default_user(*args, **kwargs):
    User.objects.create_user(USERNAME, EMAIL, PASSWORD)


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0008_alter_user_username_max_length"),
    ]

    operations = [
        migrations.RunPython(create_default_user)
    ]