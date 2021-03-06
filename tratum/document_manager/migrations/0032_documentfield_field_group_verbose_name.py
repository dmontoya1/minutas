# Generated by Django 2.0.6 on 2018-07-03 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0031_documentfield_field_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfield',
            name='field_group_verbose_name',
            field=models.CharField(blank=True, help_text='Corresponde a la palabra en singular que indica la referencia de la agrupación            Ej: Socio, Empresa, Actividad', max_length=255, null=True, verbose_name='Nombre singular de la agrupación'),
        ),
    ]
