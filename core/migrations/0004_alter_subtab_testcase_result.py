# Generated by Django 4.1.3 on 2022-11-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_requirementfilter_filter_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtab',
            name='testcase_result',
            field=models.TextField(choices=[('Pass', 'True'), ('False', 'False')]),
        ),
    ]
