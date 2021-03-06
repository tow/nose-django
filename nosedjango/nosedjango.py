"""
nose plugin for easy testing of django projects and apps. Sets up a test
database (or schema) and installs apps from test settings file before tests
are run, and tears the test database (or schema) down after all tests are run.
"""

import os, sys
import re

from nose.plugins import Plugin
import nose.case

# Force settings.py pointer
# search the current working directory and all parent directories to find
# the settings file
from nose.importer import add_path
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import re
NT_ROOT = re.compile(r"^[a-zA-Z]:\\$")
def get_SETTINGS_PATH():
    '''
    Hunt down the settings.py module by going up the FS path
    '''
    cwd = os.getcwd()
    while cwd:
        if 'settings.py' in os.listdir(cwd):
            break
        cwd = os.path.split(cwd)[0]
        if os.name == 'nt' and NT_ROOT.match(cwd):
            return None
        elif cwd == '/':
            return None
    return cwd

SETTINGS_PATH = get_SETTINGS_PATH()


class NoseDjango(Plugin):
    """
    Enable to set up django test environment before running all tests, and
    tear it down after all tests.

    Note that your django project must be on PYTHONPATH for the settings file
    to be loaded. The plugin will help out by placing the nose working dir
    into sys.path if it isn't already there, unless the -P
    (--no-path-adjustment) argument is set.
    """
    name = 'django'

    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        parser.add_option('--django-use-tags', action='store_true',
                          dest='django_use_tags', default=False,
                          help='Don\'t run all tests within django '
                               'environment; only those tagged '
                               'appropriately.')
        parser.add_option('--django-include-tag', action='store',
                          dest='django_include_tag',
                          default=env.get('NOSE_DJANGO_INCLUDE_TAG', self.name),
                          help='When django-use-tags is on, only run '
                               'django setup for tests tagged '
                               'with NOSE_DJANGO_INCLUDE_TAG (default is \'django\')')
        parser.add_option('--django-clobber-test-db', action='store',
                          dest='django_clobber_test_db',
                          default=False,
                          help='Use this flag to stop django complaining about overwriting existing test db')

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        self.verbosity = conf.verbosity
        self.django_use_tags = options.django_use_tags
        self.django_include_tag = options.django_include_tag
        self.django_clobber_test_db = options.django_clobber_test_db

    def begin(self):
        """Create the test database and schema, if needed, and switch the
        connection over to that database. Then call install() to install
        all apps listed in the loaded settings module.
        """
        # Add the working directory (and any package parents) to sys.path
        # before trying to import django modules; otherwise, they won't be
        # able to find project.settings if the working dir is project/ or
        # project/..

        if not SETTINGS_PATH:
            sys.stderr.write("Can't find Django settings file!\n")
            # short circuit if no settings file can be found
            return

        if self.conf.addPaths:
            map(add_path, self.conf.where)

        add_path(SETTINGS_PATH)
        sys.path.append(SETTINGS_PATH)
        import settings

        # Some Django code paths evaluate differently
        # between DEBUG and not DEBUG.  Example of this include the url
        # dispatcher when 404's are hit.  Django's own test runner forces DEBUG
        # to be off.
        settings.DEBUG = False 

        from django.core import mail
        self.mail = mail
        from django.conf import settings
        from django.core import management
        from django.core.management import call_command
        from django.test.utils import setup_test_environment
        from django.db import connection

        self.old_db = settings.DATABASE_NAME

        # setup the test env for each test case
        setup_test_environment()
        connection.creation.create_test_db(verbosity=self.verbosity,
            autoclobber=self.django_clobber_test_db)
        if 'south' in settings.INSTALLED_APPS:
            call_command(name='migrate', verbosity=self.verbosity)

        # exit the setup phase and let nose do it's thing

    def _django_enabled(self, test):
        if not self.django_use_tags:
            return True
        django_enabled_method = getattr(
            getattr(test.test, test.test._testMethodName),
                    self.django_include_tag, False)
        if isinstance(test.test, nose.case.MethodTestCase):
            testclass = test.test.cls()
        else:
            testclass = test.test
        django_enabled_class = getattr(testclass, self.django_include_tag, False)
        return django_enabled_method or django_enabled_class

    def beforeTest(self, test):

        if not SETTINGS_PATH or not self._django_enabled(test):
            # short circuit if no settings file can be found
            return

        # This is a distinctive difference between the NoseDjango
        # test runner compared to the plain Django test runner.
        # Django uses the standard unittest framework and resets the 
        # database between each test *suite*.  That usually resolves
        # into a test module.
        #
        # The NoseDjango test runner will reset the database between *every*
        # test case.  This is more in the spirit of unittesting where there is
        # no state information passed between individual tests.

        from django.core.management import call_command
        from django.core.urlresolvers import clear_url_caches
        from django.conf import settings
        call_command('flush', verbosity=0, interactive=False)

        if isinstance(test, nose.case.Test) and \
            isinstance(test.test, nose.case.MethodTestCase) and \
            hasattr(test.context, 'fixtures'):
                # We have to use this slightly awkward syntax due to the fact
                # that we're using *args and **kwargs together.
                call_command('loaddata', *test.context.fixtures, **{'verbosity': 0}) 

        if isinstance(test, nose.case.Test) and \
            isinstance(test.test, nose.case.MethodTestCase) and \
            hasattr(test.context, 'urls'):
                # We have to use this slightly awkward syntax due to the fact
                # that we're using *args and **kwargs together.
                self.old_urlconf = settings.ROOT_URLCONF
                settings.ROOT_URLCONF = self.urls
                clear_url_caches()

        self.mail.outbox = []

    def finalize(self, result=None):
        """
        Clean up any created database and schema.
        """
        if not SETTINGS_PATH:
            # short circuit if no settings file can be found
            return

        from django.test.utils import teardown_test_environment
        from django.db import connection
        from django.conf import settings
        connection.creation.destroy_test_db(self.old_db, verbosity=self.verbosity)   
        teardown_test_environment()

        if hasattr(self, 'old_urlconf'):
            settings.ROOT_URLCONF = self.old_urlconf
            clear_url_caches()

