# Generated by Django 5.2.3 on 2025-07-16 08:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('appointments', '0001_initial'),
        ('diagnosis', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosis',
            name='date',
        ),
        migrations.RemoveField(
            model_name='diagnosis',
            name='disease',
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appointments.appointment'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='diagnosed_disease',
            field=models.CharField(default='exit', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='prediction',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='symptoms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.doctor'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnoses', to=settings.AUTH_USER_MODEL),
        ),
    ]
