from datetime import date
from django import template
from django.conf import settings

from website.models import PersonPage

register = template.Library()


# Person feed for home page
@register.inclusion_tag(
    'website/tags/person_listing_homepage.html',
    takes_context=True
)
def person_listing_homepage(context, count=2):
    people = PersonPage.objects.filter(live=True).order_by('?')
    return {
        'people': people[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

