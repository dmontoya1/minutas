# Generated by Django 2.0.6 on 2018-08-09 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0047_auto_20180809_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfieldoption',
            name='name',
            field=models.TextField(blank=True, null=True, verbose_name='Nombre'),
        ),
    ]