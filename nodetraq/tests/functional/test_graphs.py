from nodetraq.tests import *

class TestDrrawController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='drraw', action='index'))
        # Test response...
