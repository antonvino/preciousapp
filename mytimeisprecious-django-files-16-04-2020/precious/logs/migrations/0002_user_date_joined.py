# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2015, 9, 5, 3, 42, 17, 740837, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
