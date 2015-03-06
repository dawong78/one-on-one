# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0006_auto_20150306_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 6, 9, 52, 32, 827644)),
            preserve_default=True,
        ),
    ]
