# Generated by Django 5.0.6 on 2024-05-22 06:05

from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin_user(apps, schema_editor):
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin@secure'
    )
    admin_user.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]