# Generated by Django 3.2.10 on 2022-01-06 21:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_subscription_leads_orderd_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='expire',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
