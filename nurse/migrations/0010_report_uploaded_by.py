# Generated by Django 4.0.4 on 2022-05-31 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0009_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='uploaded_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
