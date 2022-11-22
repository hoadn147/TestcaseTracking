# Generated by Django 4.1.3 on 2022-11-22 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='requirementFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req_id', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
            options={
                'db_table': 'requirement_filter',
            },
        ),
        migrations.CreateModel(
            name='subTab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcase_id', models.IntegerField()),
                ('req_id', models.IntegerField()),
                ('testcase_result', models.TextField(max_length=255)),
                ('parent_tab', models.CharField(choices=[('UNIT', 'Unit'), ('COMPLETE', 'Complete'), ('COMPONENT', 'Component'), ('DOMAIN', 'Domain')], max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
            options={
                'db_table': 'sub_tab',
                'unique_together': {('testcase_id', 'req_id'), ('user_id', 'parent_tab')},
            },
        ),
    ]
