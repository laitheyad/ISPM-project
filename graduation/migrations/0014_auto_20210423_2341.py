# Generated by Django 3.2 on 2021-04-23 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0013_auto_20210423_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='project_degree',
            new_name='level',
        ),
        migrations.AddField(
            model_name='project',
            name='project_degree',
            field=models.IntegerField(default=0, max_length=1),
            preserve_default=False,
        ),
    ]