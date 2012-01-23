import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import SimServerViews
        request = testing.DummyRequest()
        info = SimServerViews(request).site_view()
        import ipdb; ipdb.set_trace()
        self.assertEqual(info['result'], None)
        self.assertEqual(info['error'], None)
