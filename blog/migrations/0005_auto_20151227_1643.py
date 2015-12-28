# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20151227_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default=b'Anonymous', max_length=50),
        ),
    ]
