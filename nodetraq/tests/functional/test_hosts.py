from nodetraq.tests import *

class TestHostsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='hosts', action='index'))
        # Test response...
