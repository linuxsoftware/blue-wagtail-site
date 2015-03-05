# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
        ('adverts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('text', models.CharField(max_length=255)),
                ('page', models.ForeignKey(null=True, related_name='adverts', to='wagtailcore.Page', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdvertPlacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('advert', models.ForeignKey(to='adverts.Advert', related_name='+')),
                ('page', modelcluster.fields.ParentalKey(to='wagtailcore.Page', related_name='advert_placements')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
