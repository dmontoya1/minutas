# Generated by Django 2.0.6 on 2018-06-12 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_info', '0003_auto_20180612_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='policy',
            old_name='police_type',
            new_name='policy_type',
        ),
    ]
