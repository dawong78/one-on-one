# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='pairs',
            new_name='exlusions',
        ),
    ]
