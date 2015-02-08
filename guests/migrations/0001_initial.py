# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('mobile', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32, blank=True)),
                ('age', models.IntegerField(default=18, blank=True)),
                ('created_at', models.DateTimeField()),
                ('dob', models.DateTimeField(null=True, blank=True)),
                ('restuarants', jsonfield.fields.JSONField(default={b'visited': []})),
                ('last_visited', jsonfield.fields.JSONField(default={b'date': b'', b'restuarant': b''})),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('waiting_time', models.IntegerField(default=0, max_length=2, blank=True)),
                ('status', models.IntegerField(default=0)),
                ('table_no', models.CharField(default=b'0', max_length=32)),
                ('current', models.CharField(default=b'null', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('restuarant', models.CharField(max_length=32, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('guest', models.ForeignKey(to='guests.Guest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
