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
        self.assertEqual(info['result'], None)
        self.assertEqual(info['error'], None)
