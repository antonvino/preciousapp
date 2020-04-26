# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0009_auto_20150905_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 9, 10, 8, 15, 26, 833102, tzinfo=utc), verbose_name=b'Log date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='day',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Date synced'),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('date', 'author')]),
        ),
        migrations.RemoveField(
            model_name='day',
            name='day',
        ),
        migrations.RemoveField(
            model_name='day',
            name='month',
        ),
        migrations.RemoveField(
            model_name='day',
            name='year',
        ),
    ]
