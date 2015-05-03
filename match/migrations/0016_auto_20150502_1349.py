# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0015_auto_20150413_0457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pair',
            options={'ordering': ('group__name', 'person1__user__username', 'person2__user__username')},
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(related_name='group.owner', default=7, to='match.Person'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='people',
            field=models.ManyToManyField(related_name='group.people', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='person1',
            field=models.ForeignKey(related_name='match.person1', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='person2',
            field=models.ForeignKey(related_name='match.person2', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='person3',
            field=models.ForeignKey(related_name='match.person3', to='match.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pair',
            name='person1',
            field=models.ForeignKey(related_name='pair.person1', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pair',
            name='person2',
            field=models.ForeignKey(related_name='pair.person2', to='match.Person'),
            preserve_default=True,
        ),
    ]
