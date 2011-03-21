from nodetraq.tests import *

class TestInventoryController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='inventory', action='index'))
        # Test response...
