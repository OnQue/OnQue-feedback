# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='feed_match',
            field=models.IntegerField(default=141, max_length=4, null=True, editable=False),
        ),
    ]
