# ------------------------------------------------------------------------------
# Website Models
# ------------------------------------------------------------------------------

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.management import call_command
from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import AbstractImage, AbstractRendition
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from django.utils.translation import ugettext_lazy  as _
from django.db.models.signals import pre_delete, pre_save
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from wagtail.wagtailimages.feature_detection import opencv_available
from django.utils.safestring import mark_safe
from django.utils.html import escape
from .misc import CopyrightLicenses

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)

# ------------------------------------------------------------------------------
# Website Images
# ------------------------------------------------------------------------------
class WebImage(AbstractImage):
    LicenseChoices = [(code, name) for code, name, _ in CopyrightLicenses]
    author  = models.CharField(max_length=80, blank=True)
    source  = models.URLField(blank=True,
                              help_text="URL to the source, leave blank if "
                                        "the image source is not on the web")
    license = models.CharField(max_length=80, blank=True,
                               choices=LicenseChoices)
    notes   = models.CharField(max_length=251, blank=True)

class WebRendition(AbstractRendition):
    image = models.ForeignKey('WebImage', related_name='renditions')
    @property
    def attrs(self):
        title = escape(self.image.title)
        if self.image.author:
            attribution = "%s, by %s" % (title, escape(self.image.author))
        else:
            attribution = title
        return mark_safe('src="%s" width="%d" height="%d" alt="%s" title="%s"' %
                         (escape(self.url), self.width, self.height,
                          title, attribution))

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )

# Do smartcropping calculations when user saves an image without a focal point
@receiver(pre_save, sender=WebImage)
def image_feature_detection(sender, instance, **kwargs):
    if getattr(settings, 'WAGTAILIMAGES_FEATURE_DETECTION_ENABLED', False):
        if not opencv_available:
            raise ImproperlyConfigured("pyOpenCV could not be found.")
        if not instance.has_focal_point():
            instance.set_focal_point(instance.get_suggested_focal_point())

@receiver(pre_delete, sender=WebImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)

@receiver(pre_delete, sender=WebRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# ------------------------------------------------------------------------------
# A couple of abstract classes that contain commonly used fields
# ------------------------------------------------------------------------------

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True

# ------------------------------------------------------------------------------
# Website Pages
# ------------------------------------------------------------------------------

class PlainPage(Page):
    class Meta:
        verbose_name = "Page"
        description  = "A plain page (choose this if you are unsure what "\
                       "type of page to use)"

    body = RichTextField(blank=True)

    content_panels = [FieldPanel('title', classname="full title"),
                      FieldPanel('body', classname="full"), ]

    promote_panels = [FieldPanel('slug'),
                      FieldPanel('seo_title'),
                      FieldPanel('show_in_menus'),
                      FieldPanel('search_description'), ]


class HomePageHighlight(Orderable):
    homepage = ParentalKey('website.HomePage', related_name='highlights')
    title = models.CharField("Title", max_length=80, blank=True)
    blurb = RichTextField(default='', blank=True)
    image = models.ForeignKey('website.WebImage',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+')
    page  = models.ForeignKey('wagtailcore.Page',
                              null=True,
                              blank=True,
                              related_name='+')

    panels = [FieldPanel('title', classname="full title"),
              FieldPanel('blurb', classname="full"),
              ImageChooserPanel('image'),
              PageChooserPanel('page'), ]


class HomePage(Page):
    class Meta:
        verbose_name = "Homepage"
        description  = "The first page visitors see on our website"

    banner_image = models.ForeignKey('website.WebImage',
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='+')
    banner_image.help_text = "A big wide image (at least 1440x650px) to "\
                             "grab the viewer's attention"

    welcome = RichTextField(default='', blank=True)
    welcome.help_text = "A short introductory message"
    body    = RichTextField(default='', blank=True)
    body.help_text = "An area of text for whatever you like"

HomePage.content_panels = [
    ImageChooserPanel('banner_image'),
    FieldPanel('welcome', classname="full"),
    InlinePanel(HomePage, 'highlights', label="Highlights"),
    FieldPanel('body', classname="full"),
    ]

HomePage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration")
    ]



class ContactPage(Page):
    class Meta:
        verbose_name = "ContactPage"
        description  = "This is for our contact details."

    body = RichTextField(blank=True)

    content_panels = [FieldPanel('title', classname="full title"),
                      FieldPanel('body', classname="full"), ]

    promote_panels = [FieldPanel('slug'),
                      FieldPanel('seo_title'),
                      FieldPanel('show_in_menus'),
                      FieldPanel('search_description'), ]


# Carousel items

class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'website.WebImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Standard index page

class StandardIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('website.StandardIndexPage', related_name='related_links')


class StandardIndexPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'website.WebImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(StandardIndexPage, 'related_links', label="Related links"),
]

StandardIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


# Standard page

class StandardPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('website.StandardPage', related_name='carousel_items')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('website.StandardPage', related_name='related_links')


class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'website.WebImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(StandardPage, 'carousel_items', label="Carousel items"),
    FieldPanel('body', classname="full"),
    InlinePanel(StandardPage, 'related_links', label="Related links"),
]

StandardPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


class ImageCreditsPage(Page):
    intro = RichTextField(blank=True)
    search_fields = Page.search_fields + (index.SearchField('intro'),)

    def webimages(self):
        images = WebImage.objects.all()
        return images

    content_panels = [FieldPanel('title', classname="full title"),
                      FieldPanel('intro', classname="full")]

    promote_panels = [MultiFieldPanel(Page.promote_panels,
                                      "Common page configuration")]

# ------------------------------------------------------------------------------
# Website Forms
# ------------------------------------------------------------------------------

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

FormPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(FormPage, 'form_fields', label="Form fields"),
    FieldPanel('thank_you_text', classname="full"),
    MultiFieldPanel([
        FieldPanel('to_address', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('subject', classname="full"),
    ], "Email")
]


