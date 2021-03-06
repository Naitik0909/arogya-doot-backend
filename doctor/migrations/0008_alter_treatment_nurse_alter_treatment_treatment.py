# Generated by Django 4.0.4 on 2022-05-27 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0007_bed_floor_no_bed_room_no'),
        ('doctor', '0007_remove_treatment_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='nurse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nurse.nurse'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='treatment',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
