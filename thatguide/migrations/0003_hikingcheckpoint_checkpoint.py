# Generated by Django 4.0.6 on 2022-08-16 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thatguide', '0002_hikingcheckpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='hikingcheckpoint',
            name='hike_session',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='checkpoints', to='thatguide.hikingsession'),
            preserve_default=False,
        ),
    ]
