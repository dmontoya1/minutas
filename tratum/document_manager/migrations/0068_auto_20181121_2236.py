# Generated by Django 2.0.9 on 2018-11-21 22:36

from django.db import migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0067_auto_20181121_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfieldoption',
            name='linked_fields',
            field=smart_selects.db_fields.ChainedManyToManyField(auto_choose=True, blank=True, chained_field='document', chained_model_field='document', horizontal=True, related_name='linkedfields_set', to='document_manager.DocumentField', verbose_name='Campos de la opción (si aplica)'),
        ),
    ]
