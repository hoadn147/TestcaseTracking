# Generated by Django 4.1.3 on 2022-11-26 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parenttab',
            name='tab_name',
            field=models.CharField(choices=[('UNIT', 'Unit'), ('COMPLETE', 'Complete'), ('COMPONENT', 'Component'), ('DOMAIN', 'Domain')], max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='parenttab',
            unique_together={('tab_name', 'user')},
        ),
    ]