# Generated by Django 3.2 on 2021-05-12 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0022_auto_20210512_0153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progressreport',
            name='project_supervisor',
        ),
        migrations.AddField(
            model_name='progressreport',
            name='project_supervisor',
            field=models.ManyToManyField(to='graduation.Teacher'),
        ),
    ]