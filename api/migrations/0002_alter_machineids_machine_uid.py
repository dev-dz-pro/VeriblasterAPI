# Generated by Django 3.2.10 on 2022-01-04 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineids',
            name='machine_uid',
            field=models.UUIDField(unique=True),
        ),
    ]
