from datetime import date
from collections import namedtuple
from django import template
from django.conf import settings
from django.template.loader import render_to_string
from website.models import WebImage

register = template.Library()


# settings value
@register.assignment_tag
def get_google_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_KEY', "")


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    if page.get_children().live().in_menu():
        return True
    else:
        return False


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('website/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('website/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children().live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the secondary links for the 'also in this section' links
# - either the children or siblings of the current page
@register.inclusion_tag('website/tags/secondary_menu.html', takes_context=True)
def secondary_menu(context, calling_page=None):
    pages = []
    if calling_page:
        pages = calling_page.get_children().live().in_menu()
        # If no children, get siblings instead
        if len(pages) == 0:
            pages = calling_page.get_siblings(inclusive=False).live().in_menu()
    return {
        'pages': pages,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves all live pages which are children of the calling page
#for standard index listing
@register.inclusion_tag(
    'website/tags/standard_index_listing.html',
    takes_context=True
)
def standard_index_listing(context, calling_page):
    pages = calling_page.get_children().live()
    return {
        'pages': pages,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
from website.misc import CopyrightLicenses
LicenseLinks = {code: (name, url) for code, name, url in CopyrightLicenses}

@register.simple_tag
def license_link(code):
    license = LicenseLinks.get(code)
    if license and license[1]:
        return '<a class="license" target="_blank" '\
               'href="{1}">{0}</span>'.format(*license)
    else:
        return '<span class="license">{}</span>'.format(code)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@register.inclusion_tag('website/tags/site_map.html',
                        takes_context=True)
def site_map(context):
    SiteItem = namedtuple("SiteItem", "title url level")
    site = context['request'].site
    root = site.root_page
    columns = []
    items = []
    height = 0
    for parent in root.get_children().live().in_menu():
        children = parent.get_children().live().in_menu()
        items.append(SiteItem(parent.title, parent.relative_url(site), 1))
        height += 32
        if children:
            for child in children:
                if height == 0:
                    height = 32
                    items = [SiteItem("...", parent.relative_url(site), 1)]
                items.append(SiteItem(child.title, child.relative_url(site), 2))
                height += 18
                if height > 190:
                    columns.append(items)
                    items = []
                    height = 0
        if height > 160:
            columns.append(items)
            items = []
            height = 0
    if items:
        columns.append(items)
    return {'columns': columns}

