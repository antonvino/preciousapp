# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0014_auto_20150919_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField(null=True, verbose_name=b'IP address')),
                ('downloaded_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Date')),
            ],
        ),
    ]
