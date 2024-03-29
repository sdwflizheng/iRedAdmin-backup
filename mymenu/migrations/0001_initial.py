# Generated by Django 2.0 on 2018-01-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='菜单名')),
                ('menuurl', models.CharField(max_length=150, verbose_name='url地址')),
                ('menupid', models.IntegerField(verbose_name='父ID')),
                ('menuseq', models.IntegerField(verbose_name='菜单排序')),
                ('menupath', models.CharField(max_length=100, verbose_name='菜单级别序号,父id,使用逗号分割')),
                ('menutype', models.IntegerField(verbose_name='菜单类型 1、菜单 2、功能')),
            ],
        ),
    ]
