from nodetraq.tests import *

class TestToolsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='tools', action='index'))
        # Test response...
