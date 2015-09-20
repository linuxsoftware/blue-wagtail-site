#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

    from django.core.management.commands import runserver
    runserver.DEFAULT_PORT = "8110"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
