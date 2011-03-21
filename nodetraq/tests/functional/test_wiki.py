from nodetraq.tests import *

class TestWikiController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='wiki', action='index'))
        # Test response...
