# Generated by Django 4.1.3 on 2022-11-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_requirementfilter_filter_name_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementfilter',
            name='req_id',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='subtab',
            name='req_id',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='subtab',
            name='testcase_id',
            field=models.TextField(max_length=255),
        ),
    ]
