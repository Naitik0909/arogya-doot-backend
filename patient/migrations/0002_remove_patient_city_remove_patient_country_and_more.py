# Generated by Django 4.0.4 on 2022-04-26 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0002_alter_bed_bed_type'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='city',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='country',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='state',
        ),
        migrations.AddField(
            model_name='patient',
            name='aadhaar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='allocated_bed',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nurse.bed'),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_relation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='nurses',
            field=models.ManyToManyField(blank=True, to='nurse.nurse'),
        ),
    ]
