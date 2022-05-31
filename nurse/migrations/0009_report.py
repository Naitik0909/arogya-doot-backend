# Generated by Django 4.0.4 on 2022-05-31 18:18

from django.db import migrations, models
import django.db.models.deletion
import nurse.models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_remove_patient_nurses_patient_is_treated_and_more'),
        ('nurse', '0008_alter_nurse_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(blank=True, max_length=50, null=True)),
                ('report_file', models.FileField(blank=True, null=True, upload_to=nurse.models.user_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
            ],
        ),
    ]
