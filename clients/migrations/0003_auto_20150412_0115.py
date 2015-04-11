# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20150208_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='feed_match',
            field=models.IntegerField(default=689, max_length=4, null=True, editable=False),
        ),
    ]
