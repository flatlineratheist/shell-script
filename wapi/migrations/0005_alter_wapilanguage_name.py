# Generated by Django 4.1.7 on 2023-03-03 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapi', '0004_wapilanguage_wapiquestion_wapiquestiontype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wapilanguage',
            name='name',
            field=models.CharField(default='NA', max_length=30, unique=True),
        ),
    ]
