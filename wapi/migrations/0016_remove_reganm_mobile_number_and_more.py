# Generated by Django 4.1.7 on 2023-03-27 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wapi', '0015_alter_reganm_annual_lactating_women_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reganm',
            name='mobile_number',
        ),
        migrations.RemoveField(
            model_name='regasha',
            name='mobile_number',
        ),
        migrations.RemoveField(
            model_name='regbeneficiary',
            name='mobile_number',
        ),
    ]