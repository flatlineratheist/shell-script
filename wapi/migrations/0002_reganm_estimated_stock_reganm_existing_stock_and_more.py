# Generated by Django 4.1.7 on 2023-03-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reganm',
            name='estimated_stock',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='existing_stock',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='no_lactating_women',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='reganm',
            name='no_pragnant_women',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='regasha',
            name='estimated_stock',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='regasha',
            name='existing_stock',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='regasha',
            name='no_lactating_women',
            field=models.CharField(default='NA', max_length=30),
        ),
        migrations.AddField(
            model_name='regasha',
            name='no_pragnant_women',
            field=models.CharField(default='NA', max_length=30),
        ),
    ]