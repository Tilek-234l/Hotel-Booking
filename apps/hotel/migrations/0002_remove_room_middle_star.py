# Generated by Django 4.2.1 on 2023-06-27 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='middle_star',
        ),
    ]
