# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0016_auto_20150502_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentialsmodel',
            name='id',
        ),
        migrations.DeleteModel(
            name='CredentialsModel',
        ),
        migrations.RemoveField(
            model_name='flowmodel',
            name='id',
        ),
        migrations.DeleteModel(
            name='FlowModel',
        ),
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(related_name='group.owner', to='match.Person', null=True),
            preserve_default=True,
        ),
    ]
