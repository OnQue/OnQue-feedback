# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=10)),
                ('service', models.IntegerField(null=True, blank=True)),
                ('ambience', models.IntegerField(null=True, blank=True)),
                ('food', models.IntegerField(null=True, blank=True)),
                ('overall_exp', models.IntegerField(null=True, blank=True)),
                ('staff_friend', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=10)),
                ('service', models.IntegerField(null=True, blank=True)),
                ('ambience', models.IntegerField(null=True, blank=True)),
                ('food', models.IntegerField(null=True, blank=True)),
                ('overall_exp', models.IntegerField(null=True, blank=True)),
                ('staff_friend', models.IntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=32, null=True, blank=True)),
                ('dob', models.CharField(max_length=10, null=True, blank=True)),
                ('anniversary', models.CharField(max_length=10, null=True, blank=True)),
                ('comments', models.CharField(max_length=200, null=True, blank=True)),
                ('recieve_info', models.BooleanField(default=True)),
                ('table_num', models.CharField(default=b'0', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rest_name', models.CharField(max_length=32, null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=32, null=True, blank=True)),
                ('age', models.IntegerField(max_length=2)),
                ('conversion', models.BooleanField(default=False)),
                ('bill', models.IntegerField(max_length=10, null=True, blank=True)),
                ('table_num', models.CharField(default=b'0', max_length=32)),
                ('waiting', models.BooleanField(default=True)),
                ('seated', models.BooleanField(default=False)),
                ('directly_seated', models.BooleanField(default=False)),
                ('take_away', models.BooleanField(default=False)),
                ('no_show', models.BooleanField(default=False)),
                ('feed_match', models.IntegerField(default=837, max_length=4, null=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='table',
            fields=[
                ('user', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=32, null=True, blank=True)),
                ('first_name', models.CharField(max_length=32, null=True, blank=True)),
                ('last_name', models.CharField(max_length=32, null=True, blank=True)),
                ('email', models.EmailField(max_length=60, null=True, blank=True)),
                ('city', models.CharField(max_length=32, null=True, blank=True)),
                ('mobile', models.CharField(max_length=10, null=True, blank=True)),
                ('rest_name', models.CharField(max_length=32, null=True, blank=True)),
                ('n_of_table', models.IntegerField(default=0)),
                ('status', jsonfield.fields.JSONField()),
                ('waiting_list', jsonfield.fields.JSONField(default={b'waiting_list': []}, null=True)),
                ('seated', jsonfield.fields.JSONField(default={b'seated': []}, null=True)),
                ('first_login', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedbackservice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='record',
            field=models.ForeignKey(to='clients.Record', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
