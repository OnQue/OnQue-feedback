# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0003_auto_20150412_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_type', models.IntegerField(null=True)),
                ('question_text', models.CharField(max_length=1024, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RatingTexts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_text', models.CharField(default=b'Service', max_length=64, null=True)),
                ('ambience_text', models.CharField(default=b'Ambience', max_length=64, null=True)),
                ('food_text', models.CharField(default=b'Food', max_length=64, null=True)),
                ('overall_exp_text', models.CharField(default=b'Overall Experience', max_length=64, null=True)),
                ('staff_friend_text', models.CharField(default=b'Staff Friendliness', max_length=64, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(to='clients.Questions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answers',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='feedbackservice',
            name='anniversary',
        ),
        migrations.RemoveField(
            model_name='feedbackservice',
            name='recieve_info',
        ),
        migrations.AlterField(
            model_name='record',
            name='feed_match',
            field=models.IntegerField(default=716, max_length=4, null=True, editable=False),
        ),
    ]
