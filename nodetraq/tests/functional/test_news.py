from nodetraq.tests import *

class TestNewsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='news', action='index'))
        # Test response...
