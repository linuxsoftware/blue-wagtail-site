# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0002_initial_data'),
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventIndexPageRelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('date_from', models.DateField(verbose_name='Start date')),
                ('date_to', models.DateField(blank=True, verbose_name='End date', null=True, help_text='Leave this empty if the event is on a single day')),
                ('time_from', models.TimeField(blank=True, verbose_name='Start time', null=True)),
                ('time_to', models.TimeField(blank=True, verbose_name='End time', null=True)),
                ('event_type', models.CharField(choices=[('meeting', 'Committee Meeting'), ('event', 'Event'), ('group', 'Group Activity'), ('private', 'Private'), ('other', 'Other')], max_length=255)),
                ('group', models.CharField(blank=True, verbose_name='Group/Committee', choices=[('propfin', 'Property & Finance Committee'), ('fundr', 'Fundraising Committee'), ('comms', 'Communications Committee')], max_length=255)),
                ('speaker', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('cost', models.CharField(blank=True, max_length=255)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventPageRelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(to='wagtaildocs.Document', null=True, related_name='+', blank=True)),
                ('link_page', models.ForeignKey(to='wagtailcore.Page', null=True, related_name='+', blank=True)),
                ('page', modelcluster.fields.ParentalKey(to='events.EventPage', related_name='related_links')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
    ]
