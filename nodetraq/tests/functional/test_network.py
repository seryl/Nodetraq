from nodetraq.tests import *

class TestNetworkController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='network', action='index'))
        # Test response...
