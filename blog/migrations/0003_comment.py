# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151211_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('author', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2015, 12, 27, 12, 51, 30, 790770, tzinfo=utc))),
                ('parent_comment', models.ForeignKey(blank=True, to='blog.Comment', null=True)),
                ('post', models.ForeignKey(to='blog.Post')),
            ],
        ),
    ]
