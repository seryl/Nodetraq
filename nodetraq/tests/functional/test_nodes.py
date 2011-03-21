from nodetraq.tests import *

class TestNodesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='nodes', action='index'))
        # Test response...
