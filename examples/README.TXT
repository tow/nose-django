If you change directory into the 'project' directory, you should be able  to
run the nose test runner and get reasonable results.


Something like this:

    C:\dev\nosedjango\examples\project>nosetests -v --with-django
    project.tests.test_views.test_view_index ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 0.047s

    OK
    Destroying test database...

    C:\dev\nosedjango\examples\project>


