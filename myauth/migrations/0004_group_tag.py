# Generated by Django 2.0 on 2018-01-22 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0003_auto_20180119_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='tag',
            field=models.CharField(default='unknow', max_length=30, verbose_name='用于业务识别标签'),
        ),
    ]
