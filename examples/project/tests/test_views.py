from django.test.client import Client

def test_view_index():
    c = Client()
    resp = c.get('/zoo/')
    assert "Just a title" in resp.content
    assert "foobar" in resp.content
