# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PairState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match_count', models.IntegerField()),
                ('pair', models.ForeignKey(to='match.Pair')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unmatched_count', models.IntegerField()),
                ('crowd_count', models.IntegerField()),
                ('person', models.ForeignKey(to='match.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('group', models.ForeignKey(to='match.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pair',
            name='person1',
            field=models.ForeignKey(related_name='first_person_pair', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pair',
            name='person2',
            field=models.ForeignKey(related_name='second_person_pair', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='person1',
            field=models.ForeignKey(related_name='first_person_match', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='person2',
            field=models.ForeignKey(related_name='second_person_match', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='person3',
            field=models.ForeignKey(related_name='third_person_match', to='match.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='result',
            field=models.ForeignKey(to='match.Result'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='pairs',
            field=models.ManyToManyField(to='match.Pair'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='people',
            field=models.ManyToManyField(to='match.Person'),
            preserve_default=True,
        ),
    ]
