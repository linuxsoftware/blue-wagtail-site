# ------------------------------------------------------------------------------
# Events
# ------------------------------------------------------------------------------
from datetime import date
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from events.utils import export_event
from django.db import models


from website.models import RelatedLink
from website.models import WebImage

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)

EVENT_TYPES = (
    ('meeting',  "Committee Meeting"),
    ('event',    "Event"),
    ('group',    "Group Activity"),
    ('private',  "Private"),
    ('other',    "Other"),
)

# TODO store groups in db
# Use GroupPage?
# or...
#class Groups(models.Model):
#    code = models.CharField(max_length=12)
#    name = models.CharField(max_length=100)

GROUPS = (
    ('propfin', "Property & Finance Committee"),
    ('fundr',   "Fundraising Committee"),
    ('comms',   "Communications Committee"),
)

# Event index page

class EventIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('events.EventIndexPage', related_name='related_links')


class EventIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    @property
    def events(self):
        # Get list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        events = events.filter(date_from__gte=date.today())

        # Order by date
        events = events.order_by('date_from')

        return events

EventIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(EventIndexPage, 'related_links', label="Related links"),
]

EventIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Event page

class EventPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('events.EventPage', related_name='related_links')


class EventPage(Page):
    date_from = models.DateField("Start date")
    date_to = models.DateField("End date", null=True, blank=True)
    date_to.help_text="Leave this empty if the event is on a single day"
    time_from = models.TimeField("Start time", null=True, blank=True)
    time_to = models.TimeField("End time", null=True, blank=True)
    event_type = models.CharField(max_length=255, choices=EVENT_TYPES)
    group = models.CharField("Group/Committee", choices=GROUPS,
                             max_length=255, blank=True)
    speaker = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey('website.WebImage',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+')
    cost = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('location'),
        index.SearchField('body'),
    )

    def clean(self):
        super().clean()
        if self.date_to is None:
            self.date_to = self.date_from


    @property
    def event_index(self):
        # Find closest ancestor which is an event index
        return self.get_ancestors().type(EventIndexPage).last()

    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                response = HttpResponse(export_event(self, 'ical'),
                                        content_type='text/calendar')
                response['Content-Disposition'] = \
                    'attachment; filename={}.ics'.format(self.slug)
                return response
            else:
                # Unrecognised format error
                return HttpResponse('Could not export event\n\n'
                                    'Unrecognised format: {}'.
                                        format(request.GET['format']),
                                    content_type='text/plain')
        else:
            # Display event page as usual
            return super(EventPage, self).serve(request)

EventPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('event_type'),
    ImageChooserPanel('image'),
    FieldPanel('date_from'),
    FieldPanel('date_to'),
    FieldPanel('time_from'),
    FieldPanel('time_to'),
    FieldPanel('body', classname="full"),
    FieldPanel('speaker'),
    FieldPanel('group'),
    FieldPanel('location'),
    FieldPanel('cost'),
    InlinePanel(EventPage, 'related_links', label="Related links"),
]

EventPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]

