from nodetraq.tests import *

class TestPoolsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pools', action='index'))
        # Test response...
