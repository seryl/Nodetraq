from nodetraq.tests import *

class TestPuppetController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='puppet', action='index'))
        # Test response...
