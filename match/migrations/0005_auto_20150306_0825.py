# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_auto_20150306_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='name',
        ),
        migrations.AlterField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 6, 8, 25, 57, 701236)),
            preserve_default=True,
        ),
    ]
