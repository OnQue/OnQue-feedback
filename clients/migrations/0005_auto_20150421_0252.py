# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20150421_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='show',
            field=models.IntegerField(default=1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ratingtexts',
            name='food_text',
            field=models.CharField(default=b'Quality of Food', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='ratingtexts',
            name='service_text',
            field=models.CharField(default=b'Quality of Service', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='feed_match',
            field=models.IntegerField(default=702, max_length=4, null=True, editable=False),
        ),
    ]
