# Generated by Django 5.1 on 2025-04-08 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Services', '0004_companyservice_explanation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyservice',
            name='explanation',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
