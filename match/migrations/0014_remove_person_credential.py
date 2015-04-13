# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0013_person_credential'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='credential',
        ),
    ]
