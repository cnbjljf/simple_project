# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 00:09
from __future__ import unicode_literals

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Simple_BBS', '0004_userprofile_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='head_img',
            field=models.ImageField(default=builtins.dir, upload_to='upload', verbose_name='文章图像'),
            preserve_default=False,
        ),
    ]
