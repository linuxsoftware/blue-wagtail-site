from django import template
from website.models import Advert

register = template.Library()


# Advert snippets
@register.inclusion_tag('adverts/tags/adverts.html', takes_context=True)
def adverts(context):
    return {
        'adverts': Advert.objects.all(),
        'request': context['request'],
    }

