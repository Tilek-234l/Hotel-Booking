# Generated by Django 4.2.1 on 2023-06-27 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_remove_room_middle_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/room_photos/', verbose_name='Hotels_Image'),
        ),
        migrations.AlterField(
            model_name='room',
            name='is_booked',
            field=models.BooleanField(default=False, verbose_name='Is Booked'),
        ),
    ]
