# Generated by Django 4.1.7 on 2023-03-21 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapi', '0012_regasha_first_trimester_regasha_lakshit_dumpati_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reganm',
            name='first_trimester',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='lakshit_dumpati',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='no_cal',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='no_folic_acid',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='no_ifa',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='second_third_trimester',
            field=models.CharField(default='NA', max_length=30),
        ),
    ]
