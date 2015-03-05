from datetime import date, timedelta, time
from django import template
from django.conf import settings
from website.models import WebImage


from events.models import EventPage

register = template.Library()


# Events feed for home page
@register.inclusion_tag('events/tags/event_listing_homepage.html',
                        takes_context=True)
def event_listing_homepage(context, count=2):
    events = EventPage.objects.filter(live=True)
    events = events.filter(date_from__gte=date.today()).order_by('date_from')
    return {
        'events': events[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

@register.inclusion_tag('events/tags/events_this_week.html',
                        takes_context=True)
def events_this_week(context, count=2):
    today = date.today()
    begin_ord = today.toordinal()
    if today.weekday() != 6:
        # Start week with Monday, unless today is Sunday
        begin_ord -= today.weekday()
    end_ord = begin_ord + 7
    weekdays = [date.fromordinal(ord) for ord in range(begin_ord, end_ord)]
    events_in_week = EventPage.objects.live()                       \
                              .filter(date_to__gte   = weekdays[0]) \
                              .filter(date_from__lte = weekdays[-1])
    events = []
    for event_day in weekdays:
        days_events = []
        continuing_events = []
        for event_in_week in events_in_week:
            if event_in_week.date_from == event_day:
                days_events.append(event_in_week)
            elif event_in_week.date_from < event_day <= event_in_week.date_to:
                continuing_events.append(event_in_week)
        days_events.sort(key=lambda event:event.time_from or time.max)
        events.append((event_day, days_events, continuing_events))

    return {'events': events, 'today':  today }



# Format times e.g. on event page
@register.filter
def time_display(time):
    # Get hour and minute from time object
    hour = time.hour
    minute = time.minute

    # Convert to 12 hour format
    if hour >= 12:
        pm = True
        hour -= 12
    else:
        pm = False
    if hour == 0:
        hour = 12

    # Hour string
    hour_string = str(hour)

    # Minute string
    if minute != 0:
        minute_string = "." + str(minute)
    else:
        minute_string = ""

    # PM string
    if pm:
        pm_string = "pm"
    else:
        pm_string = "am"

    # Join and return
    return "".join([hour_string, minute_string, pm_string])



