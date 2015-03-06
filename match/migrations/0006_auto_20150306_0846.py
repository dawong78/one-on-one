# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_auto_20150306_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='person3',
            field=models.ForeignKey(related_name='third_person_match', to='match.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 6, 8, 46, 19, 309843)),
            preserve_default=True,
        ),
    ]
