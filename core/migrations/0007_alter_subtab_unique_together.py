# Generated by Django 4.1.3 on 2022-11-24 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_user_id_subtab_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subtab',
            unique_together={('testcase_id', 'req_id')},
        ),
    ]
