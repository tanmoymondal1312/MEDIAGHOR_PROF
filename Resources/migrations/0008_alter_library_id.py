# Generated by Django 5.1 on 2025-04-06 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Resources', '0007_alter_library_short_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='id',
            field=models.SlugField(editable=False, max_length=60, primary_key=True, serialize=False, unique=True),
        ),
    ]
