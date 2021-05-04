# Generated by Django 3.2 on 2021-05-04 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0014_auto_20210423_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=9),
            preserve_default=False,
        ),
    ]