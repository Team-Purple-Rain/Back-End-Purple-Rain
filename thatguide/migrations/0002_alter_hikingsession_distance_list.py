# Generated by Django 4.0.6 on 2022-08-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thatguide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hikingsession',
            name='distance_list',
            field=models.IntegerField(choices=[(1, '1 mile'), (2, '2 miles'), (3, '3 miles'), (4, '4 miles'), (5, '5 miles'), (6, '6 miles'), (7, '7 miles'), (8, '8 miles'), (9, '9 miles'), (10, '10 miles')], default=1),
        ),
    ]