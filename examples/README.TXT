The 'project' sample Django project was created using Django 1.0b1.

Using a more recent version of Django may cause problems.  You've been
warned.


If you change directory into the 'project' directory, you should be
able  to run the nose test runner and get reasonable results.

Note that you *won't* be running your doctests unless you tell nose to
do so.

As usual, you need to tell nose to run doctest test strings in modules
that contain standard test classes.

A successful run should hit *11* test cases excercising :

    * race conditions between test cases that create objects in test
      methods
    * race conditions between test cases that create objects in 
      fixture loading
    * doctests
    * test functions
    * mixes of doctests and test modules
    * docstrings in models

--- Sample test run below ---

C:\dev\nosedjango\examples\project>nosetests -v --with-django --with-doctest --doctest-tests --doctest-tests
doctest: project.zoo.models.zoo ... ok
Doctest: project.zoo.models.Zoo.__str__ ... ok
Doctest: project.zoo.models.func ... ok
This is just a stub for a regular test method ... ok
Doctest: project.zoo.test_doctest_modules.test_docstring ... ok
Doctest: project.zoo.test_doctest_modules.test_docstring ... ok
project.zoo.test_fixtures.TestFixture1.test_count ... ok
project.zoo.test_fixtures.TestFixture2.test_count ... ok
project.zoo.test_race.TestDBRace1.test1 ... ok
project.zoo.test_race.TestDBRace2.test1 ... ok
project.tests.test_views.test_view_index ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.859s

OK
Destroying test database...

C:\dev\nosedjango\examples\project>
