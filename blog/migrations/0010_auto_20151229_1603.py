# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20151229_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_level',
            new_name='level',
        ),
    ]
