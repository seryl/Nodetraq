from nodetraq.tests import *

class TestVhostsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='vhosts', action='index'))
        # Test response...
