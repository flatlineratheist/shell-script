# Generated by Django 4.1.7 on 2023-03-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapi', '0009_regbeneficiary_pragnancy_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='regasha',
            name='facility_name',
            field=models.CharField(default='NA', max_length=30),
        ),
    ]
