# Generated by Django 3.2 on 2021-04-23 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0009_auto_20210423_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='group_members',
        ),
        migrations.AddField(
            model_name='project',
            name='project_supervisor',
            field=models.ManyToManyField(to='graduation.Teacher'),
        ),
    ]
