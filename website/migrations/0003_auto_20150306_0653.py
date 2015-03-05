# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
from django.conf import settings
import taggit.managers
import django.db.models.deletion
import wagtail.wagtailimages.models
import modelcluster.fields
import wagtail.wagtailadmin.taggable


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0002_initial_data'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
        ('taggit', '0001_initial'),
        ('wagtailimages', '0005_make_filter_spec_unique'),
        ('website', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'ContactPage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255)),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')], max_length=16)),
                ('required', models.BooleanField(default=True)),
                ('choices', models.CharField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512)),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255)),
                ('help_text', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to this address', max_length=255)),
                ('from_address', models.CharField(blank=True, max_length=255)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('thank_you_text', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageHighlight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(blank=True, verbose_name='Title', max_length=80)),
                ('blurb', wagtail.wagtailcore.fields.RichTextField(blank=True, default='')),
                ('homepage', modelcluster.fields.ParentalKey(to='website.HomePage', related_name='highlights')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageCreditsPage',
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
            name='PlainPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StandardIndexPage',
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
            name='StandardIndexPageRelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(to='wagtaildocs.Document', null=True, related_name='+', blank=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StandardPageCarouselItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('embed_url', models.URLField(blank=True, verbose_name='Embed URL')),
                ('caption', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StandardPageRelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_document', models.ForeignKey(to='wagtaildocs.Document', null=True, related_name='+', blank=True)),
                ('link_page', models.ForeignKey(to='wagtailcore.Page', null=True, related_name='+', blank=True)),
                ('page', modelcluster.fields.ParentalKey(to='website.StandardPage', related_name='related_links')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('file', models.ImageField(verbose_name='File', width_field='width', upload_to=wagtail.wagtailimages.models.get_upload_to, height_field='height')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=80)),
                ('source', models.URLField(blank=True, help_text='URL to the source, leave blank if the image source is not on the web')),
                ('license', models.CharField(blank=True, choices=[('CC_BY', 'Creative Commons Attrib'), ('CC_BY-SA', 'Creative Commons Attrib-ShareAlike'), ('CC_BY-ND', 'Creative Commons Attrib-NoDerivs'), ('CC_BY-NC', 'Creative Commons Attrib-NonCommercial'), ('CC_BY-NC-SA', 'Creative Commons Attrib-NonCommercial-ShareAlike'), ('CC_BY-NC-ND', 'Creative Commons Attrib-NonCommercial-NoDerivs'), ('GPL2', 'GNU Public License 2'), ('GPL3', 'GNU Public License 3'), ('GFDL', 'GNU Free Documentation License'), ('Consent', 'Proprietary: Consent granted (explain in the notes)'), ('Public', 'Public Domain'), ('morgueFile', 'morgueFile License'), ('ShtrStck', 'Shutterstock Terms of Service'), ('FDP', 'Free Digital Photos.net License'), ('Other', 'Other (Specify in the notes)')], max_length=80)),
                ('notes', models.CharField(blank=True, max_length=251)),
                ('tags', taggit.managers.TaggableManager(verbose_name='Tags', help_text=None, through='taggit.TaggedItem', to='taggit.Tag', blank=True)),
                ('uploaded_by_user', models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='WebRendition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file', models.ImageField(width_field='width', upload_to='images', height_field='height')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, editable=False, default='', max_length=255)),
                ('filter', models.ForeignKey(to='wagtailimages.Filter', related_name='+')),
                ('image', models.ForeignKey(to='website.WebImage', related_name='renditions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='webrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
        migrations.AddField(
            model_name='standardpagecarouselitem',
            name='image',
            field=models.ForeignKey(to='website.WebImage', null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardpagecarouselitem',
            name='link_document',
            field=models.ForeignKey(to='wagtaildocs.Document', null=True, related_name='+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardpagecarouselitem',
            name='link_page',
            field=models.ForeignKey(to='wagtailcore.Page', null=True, related_name='+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardpagecarouselitem',
            name='page',
            field=modelcluster.fields.ParentalKey(to='website.StandardPage', related_name='carousel_items'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardpage',
            name='feed_image',
            field=models.ForeignKey(to='website.WebImage', null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardindexpagerelatedlink',
            name='link_page',
            field=models.ForeignKey(to='wagtailcore.Page', null=True, related_name='+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardindexpagerelatedlink',
            name='page',
            field=modelcluster.fields.ParentalKey(to='website.StandardIndexPage', related_name='related_links'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='standardindexpage',
            name='feed_image',
            field=models.ForeignKey(to='website.WebImage', null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepagehighlight',
            name='image',
            field=models.ForeignKey(to='website.WebImage', null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepagehighlight',
            name='page',
            field=models.ForeignKey(to='wagtailcore.Page', null=True, related_name='+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formfield',
            name='page',
            field=modelcluster.fields.ParentalKey(to='website.FormPage', related_name='form_fields'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'Homepage'},
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_image',
            field=models.ForeignKey(to='website.WebImage', null=True, help_text="A big wide image (at least 1440x650px) to grab the viewer's attention", related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, default='', help_text='An area of text for whatever you like'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepage',
            name='welcome',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, default='', help_text='A short introductory message'),
            preserve_default=True,
        ),
    ]
