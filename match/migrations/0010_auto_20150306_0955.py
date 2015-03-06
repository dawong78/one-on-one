# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0009_auto_20150306_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
