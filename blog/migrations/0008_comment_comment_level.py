# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20151227_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_level',
            field=models.CharField(default=0, max_length=2),
        ),
    ]
