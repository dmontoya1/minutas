# Generated by Django 2.0.6 on 2018-06-28 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0030_auto_20180628_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfield',
            name='field_group',
            field=models.ManyToManyField(blank=True, related_name='_documentfield_field_group_+', to='document_manager.DocumentField', verbose_name='Campos del grupo'),
        ),
    ]
