from nodetraq.tests import *

class TestMonitorController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='monitor', action='index'))
        # Test response...
