from setuptools import setup, find_packages

setup(
    name='NoseDjango',
    version='0.5',
    author='Victor Ng',
    author_email = 'victor.ng@monkeybeanonline.com',
    description = 'nose plugin for easy testing of django projects ' \
        'and apps. Sets up a test database (or schema) and installs apps ' \
        'from test settings file before tests are run, and tears the test ' \
        'database (or schema) down after all tests are run.',
    install_requires='nose>=0.10',
    url = "http://poli-cms.googlecode.com/svn/nose-django/",
    license = 'GNU LGPL',
    packages = find_packages(exclude=['tests']),
    zip_safe = False,
    include_package_data = True,
    entry_points = {
        'nose.plugins': [
            'django = nosedjango.nosedjango:NoseDjango',
            ]
        }
    )

