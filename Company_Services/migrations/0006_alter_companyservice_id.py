# Generated by Django 5.1 on 2025-04-08 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Services', '0005_alter_companyservice_explanation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyservice',
            name='id',
            field=models.SlugField(editable=False, max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]
