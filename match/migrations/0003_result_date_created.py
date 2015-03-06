# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20150306_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 6, 7, 0, 56, 39032)),
            preserve_default=True,
        ),
    ]
