# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-11 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Simple_BBS', '0004_userprofile_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('brief', models.CharField(blank=True, max_length=255, null=True)),
                ('max_members', models.IntegerField(default=200)),
                ('admins', models.ManyToManyField(blank=True, related_name='group_admins', to='Simple_BBS.UserProfile')),
                ('members', models.ManyToManyField(blank=True, related_name='group_members', to='Simple_BBS.UserProfile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Simple_BBS.UserProfile')),
            ],
        ),
    ]
