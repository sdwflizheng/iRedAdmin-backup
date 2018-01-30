# Generated by Django 2.0 on 2018-01-15 15:50

from django.db import migrations, models
import myauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('mymenu', '0001_initial'),
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='name')),
                ('permissions', models.ManyToManyField(blank=True, to='mymenu.Menu', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
            managers=[
                ('objects', myauth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='mymenu.Menu', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='myauth.Group', verbose_name='groups'),
        ),
    ]