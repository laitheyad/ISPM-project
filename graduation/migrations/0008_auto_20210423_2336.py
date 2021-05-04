# Generated by Django 3.2 on 2021-04-23 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0007_alter_teacher_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_supervisor',
            field=models.ManyToManyField(to='graduation.Teacher'),
        ),
        migrations.AlterField(
            model_name='project',
            name='group_members',
            field=models.ManyToManyField(to='graduation.Student'),
        ),
    ]