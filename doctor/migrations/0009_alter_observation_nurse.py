# Generated by Django 4.0.4 on 2022-05-27 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0007_bed_floor_no_bed_room_no'),
        ('doctor', '0008_alter_treatment_nurse_alter_treatment_treatment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='nurse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nurse.nurse'),
        ),
    ]
