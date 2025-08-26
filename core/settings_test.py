"""
Test settings for HajjUmrahFlow project.

Overrides the database settings to use an in-memory SQLite database for tests.
"""
from .settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}