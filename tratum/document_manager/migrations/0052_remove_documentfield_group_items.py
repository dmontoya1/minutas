# Generated by Django 2.0.6 on 2018-08-22 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0051_auto_20180821_0841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfield',
            name='group_items',
        ),
    ]
