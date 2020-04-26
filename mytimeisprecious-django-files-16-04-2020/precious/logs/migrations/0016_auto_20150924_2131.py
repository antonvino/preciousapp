# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0015_download'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='ip',
            field=models.GenericIPAddressField(null=True, verbose_name=b'IP address'),
        ),
    ]
