# Generated by Django 3.2.3 on 2021-05-26 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='permissions.Permission'),
        ),
    ]