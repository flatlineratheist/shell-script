# Generated by Django 4.1.7 on 2023-03-21 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapi', '0010_regasha_facility_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wapiregistration',
            name='current_stage',
            field=models.CharField(default='NA', max_length=90),
        ),
    ]