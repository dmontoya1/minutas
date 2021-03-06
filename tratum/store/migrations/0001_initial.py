# Generated by Django 2.0.6 on 2018-06-12 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('document_manager', '0010_document_deleted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('price', models.PositiveIntegerField()),
                ('documents', models.ManyToManyField(blank=True, null=True, to='document_manager.Document', verbose_name='Documentos')),
            ],
            options={
                'verbose_name': 'Paquete de documento',
                'verbose_name_plural': 'Paquetes de documentos',
            },
        ),
    ]
