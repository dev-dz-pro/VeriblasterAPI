# Generated by Django 3.2.10 on 2022-01-05 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_machineids_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='leads_orderd',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='leads_orderd_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]