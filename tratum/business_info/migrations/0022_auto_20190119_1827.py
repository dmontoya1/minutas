# Generated by Django 2.0.9 on 2019-01-19 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_info', '0021_glossarycategory_glossaryitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryitem',
            name='word',
            field=models.CharField(max_length=100, unique=True, verbose_name='Palabra'),
        ),
    ]
