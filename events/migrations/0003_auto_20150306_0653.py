# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0002_initial_data'),
        ('events', '0002_eventindexpage_eventindexpagerelatedlink_eventpage_eventpagerelatedlink'),
        ('website', '0003_auto_20150306_0653'),
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='image',
            field=models.ForeignKey(to='website.WebImage', null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventindexpagerelatedlink',
            name='link_document',
            field=models.ForeignKey(to='wagtaildocs.Document', null=True, related_name='+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventindexpagerelatedlink',
            name='link_page',
            field=models.ForeignKey(to='wagtailcore.Page', null=True, related_name='+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventindexpagerelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(to='events.EventIndexPage', related_name='related_links'),
            preserve_default=True,
        ),
    ]
