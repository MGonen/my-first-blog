# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20151227_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=50),
        ),
    ]
