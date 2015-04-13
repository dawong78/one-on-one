# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0011_auto_20150412_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={},
        ),
        migrations.RemoveField(
            model_name='person',
            name='email',
        ),
        migrations.RemoveField(
            model_name='person',
            name='name',
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='flowmodel',
            name='id',
            field=models.ForeignKey(primary_key=True, serialize=False, to='match.Person'),
            preserve_default=True,
        ),
    ]
