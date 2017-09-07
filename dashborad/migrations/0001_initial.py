# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=11, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'idc',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=11)),
                ('title', models.CharField(max_length=32)),
                ('department', models.ForeignKey(to='dashborad.Department', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
                'default_related_name': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=32)),
                ('ip', models.CharField(unique=True, max_length=15)),
                ('cpu', models.CharField(max_length=50, null=True)),
                ('mem', models.CharField(max_length=50)),
                ('disk', models.CharField(max_length=50)),
                ('status', models.IntegerField()),
                ('loads', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'server',
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a', models.CharField(max_length=21)),
            ],
        ),
    ]
