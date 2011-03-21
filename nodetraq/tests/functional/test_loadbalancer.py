from nodetraq.tests import *

class TestLoadbalancerController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='loadbalancer', action='index'))
        # Test response...
