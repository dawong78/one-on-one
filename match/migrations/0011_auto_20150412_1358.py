# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.django_orm
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('match', '0010_auto_20150306_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credential', oauth2client.django_orm.CredentialsField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlowModel',
            fields=[
                ('id', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('flow', oauth2client.django_orm.FlowField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ('result', 'person1', 'person2', 'person3')},
        ),
        migrations.AlterModelOptions(
            name='pair',
            options={'ordering': ('group__name', 'person1__name', 'person2__name')},
        ),
        migrations.AlterModelOptions(
            name='pairstate',
            options={'ordering': ('pair',)},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('name', 'email')},
        ),
        migrations.AlterModelOptions(
            name='personstate',
            options={'ordering': ('group', 'person')},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('date_created',)},
        ),
        migrations.AlterField(
            model_name='match',
            name='result',
            field=models.ForeignKey(related_name='matches', to='match.Result'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='result',
            name='group',
            field=models.ForeignKey(related_name='results', to='match.Group'),
            preserve_default=True,
        ),
    ]
