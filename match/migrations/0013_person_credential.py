# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0012_auto_20150413_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='credential',
            field=oauth2client.django_orm.CredentialsField(null=True),
            preserve_default=True,
        ),
    ]
