from django.http import HttpRequest
from project.zoo import views

def test_view_index():
    r = views.index(HttpRequest())
    assert r
