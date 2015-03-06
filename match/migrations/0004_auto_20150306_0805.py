# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_result_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='exlusions',
        ),
        migrations.AddField(
            model_name='pair',
            name='group',
            field=models.ForeignKey(default=1, to='match.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personstate',
            name='group',
            field=models.ForeignKey(default=1, to='match.Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 6, 8, 3, 36, 373596)),
            preserve_default=True,
        ),
    ]
