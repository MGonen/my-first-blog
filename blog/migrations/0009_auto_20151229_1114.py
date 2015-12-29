# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_comment_comment_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_level',
            field=models.IntegerField(default=0),
        ),
    ]
