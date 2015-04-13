# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0014_remove_person_credential'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowmodel',
            name='id',
            field=models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
