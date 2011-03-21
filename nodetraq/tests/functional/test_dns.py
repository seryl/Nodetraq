from nodetraq.tests import *

class TestDnsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dns', action='index'))
        # Test response...
