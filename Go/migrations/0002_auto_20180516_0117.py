# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Go', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_id',
            field=models.ForeignKey(null=True, default=None, to='Go.Comment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(default='static/img/default.jpg', upload_to='media/upload/avatar'),
        ),
    ]
