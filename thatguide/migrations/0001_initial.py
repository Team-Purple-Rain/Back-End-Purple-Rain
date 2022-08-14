# Generated by Django 4.0.6 on 2022-08-14 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HikingSession',
            fields=[
                ('timestamp_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='thatguide.timestamp')),
                ('distance_list', models.IntegerField(choices=[(1, '1 mile'), (5, '5 miles'), (10, '10 miles')], default=1)),
            ],
            bases=('thatguide.timestamp',),
        ),
    ]
