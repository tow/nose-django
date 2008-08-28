If you change directory into the 'project' directory, you should be able  to
run the nose test runner and get reasonable results.

Note that you *won't* be running your doctests unless you tell nose to do so.

As usual, you need to tell nose to run doctest test strings in modules that
contain standard test classes.

A successful run should hit *7* test cases.

    C:\dev\nosedjango\examples\project>nosetests -v --with-django --with-doctest --d
    octest-tests --doctest-tests
    Doctest: project.zoo.models ... ok
    Doctest: project.zoo.models.Zoo ... ok
    Doctest: project.zoo.models.Zoo.__str__ ... ok
    Doctest: project.zoo.models.func ... ok
    This is just a stub for a regular test method ... ok
    Doctest: project.zoo.test_foo.blah ... ok
    project.tests.test_views.test_view_index ... ok

    ----------------------------------------------------------------------
    Ran 7 tests in 0.562s

    OK
    Destroying test database...
