# Generated by Django 2.0.6 on 2018-08-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0048_auto_20180809_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
    ]
