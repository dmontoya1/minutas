# Generated by Django 2.0.6 on 2018-06-26 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0026_auto_20180626_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='field_type',
            field=models.CharField(blank=True, choices=[('NU', 'Numérico'), ('TX', 'Texto abierto'), ('DT', 'Fecha'), ('SE', 'Opciones de única respuesta'), ('LI', 'Listado'), ('GP', 'Agrupación de campos')], max_length=2, null=True, verbose_name='Tipo de campo'),
        ),
    ]