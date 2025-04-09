# Generated by Django 5.1.5 on 2025-04-08 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance_app', '0001_initial'),
        ('student_app', '0001_initial'),
        ('tracker_app', '0001_initial'),
        ('trainer_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker_app.batch'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app.studentprofile'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trainer_app.trainerprofile'),
        ),
    ]
