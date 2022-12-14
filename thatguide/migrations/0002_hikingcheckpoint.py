# Generated by Django 4.0.6 on 2022-08-16 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thatguide', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HikingCheckPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.JSONField()),
                ('elevation', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
