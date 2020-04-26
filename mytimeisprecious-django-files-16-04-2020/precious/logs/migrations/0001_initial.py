# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Date')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(unique=True, max_length=255)),
                ('is_active', models.BooleanField(default=True, help_text=b'Unselect this instead of deleting accounts.', verbose_name=b'Is Active?')),
                ('is_admin', models.BooleanField(default=False, help_text=b'Select this to let users edit the website.', verbose_name=b'Is Admin?')),
                ('username', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveSmallIntegerField(default=0)),
                ('month', models.PositiveSmallIntegerField(default=0)),
                ('day', models.PositiveSmallIntegerField(default=0)),
                ('day_text', models.CharField(max_length=2000, null=True, blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date synced')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.PositiveSmallIntegerField(default=0)),
                ('productive', models.PositiveSmallIntegerField(default=1, choices=[(0, b'Bad'), (1, b'Neutral'), (2, b'Good')])),
                ('hour_text', models.CharField(max_length=300, null=True, blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date synced')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('day', models.ForeignKey(to='logs.Day')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='hour',
            unique_together=set([('day', 'hour', 'author')]),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('year', 'month', 'day', 'author')]),
        ),
    ]
