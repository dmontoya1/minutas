# Generated by Django 2.0.6 on 2018-07-25 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_userdocument_identifier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdocument',
            options={'ordering': ['-created_at'], 'verbose_name': 'Documento de usuario', 'verbose_name_plural': 'Documentos de usuarios'},
        ),
    ]