# Generated by Django 4.0.6 on 2022-08-14 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HikingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance_list', models.IntegerField(choices=[(1, '1 mile'), (5, '5 miles'), (10, '10 miles')], default=1)),
                ('start_location', models.JSONField()),
                ('end_location', models.JSONField(blank=True, null=True)),
                ('distance_traveled', models.IntegerField(blank=True, null=True)),
                ('avg_mph', models.IntegerField(blank=True, null=True)),
                ('travel_time', models.IntegerField(blank=True, null=True)),
                ('elevation_gain', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]