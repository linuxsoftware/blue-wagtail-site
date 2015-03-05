# If local.py is present, any settings in it will override those in base.py and dev.py.
# Use this for any settings that are specific to this one installation, such as developer API keys.
# local.py should not be checked in to version control.

EMBEDLY_KEY = 'get-one-from-http://embed.ly/'
GOOGLE_MAPS_KEY = 'xxxxxxxxxxXXXXXXXxxxxxxxxxXXXXXXXxxxxXx'

# It is strongly recommended that you define a SECRET_KEY here, where it won't be visible
# in your version control system.
SECRET_KEY = 'xxxxxxxXXXXXXXXxxxxxxxxXXXXXXXXXXxXXXxxxxxxxxXXXXX'

# PostgreSQL (Recommended, but requires the psycopg2 library and Postgresql development headers)
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'blue',
        'USER':     'blue',
        'PASSWORD': 'xxxxxxxx',
        'HOST': '',  # Set to empty string for localhost.
        'PORT': '',  # Set to empty string for default.
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
    }
}

# When developing Wagtail templates, we recommend django-debug-toolbar
# for keeping track of page rendering times. To use it:
#     pip install django-debug-toolbar==1.0.1
# and uncomment the lines below.

# from .base import INSTALLED_APPS, MIDDLEWARE_CLASSES
# INSTALLED_APPS += (
#     'debug_toolbar',
# )
# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
# # django-debug-toolbar settings
# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': False,
# }


# If you're developing Wagtail itself (as opposed to building a Wagtail-powered site), you'll
# want to tweak the Python path so that it picks up your working copy of the Wagtail code
# rather than the packaged copy - uncomment the lines below to do that.
# Here we assume that you have it in a 'wagtail' directory at the same level as your
# 'wagtaildemo' checkout - adjust the path as appropriate.

# import sys
# import os
# PATH_TO_WAGTAIL = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'wagtail')
# sys.path.insert(1, PATH_TO_WAGTAIL)
