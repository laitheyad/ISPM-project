# Generated by Django 3.2 on 2021-04-23 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0011_remove_project_project_supervisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='group_members',
            field=models.ManyToManyField(to='graduation.User'),
        ),
    ]
