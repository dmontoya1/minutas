# Generated by Django 2.0.6 on 2018-06-13 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0013_auto_20180612_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentfield',
            name='document',
        ),
        migrations.DeleteModel(
            name='DocumentField',
        ),
    ]
