# Generated by Django 2.0.9 on 2019-01-19 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0070_documentfieldoption_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfieldoption',
            options={'ordering': ['order'], 'verbose_name': 'Opción', 'verbose_name_plural': 'Opciones'},
        ),
    ]
