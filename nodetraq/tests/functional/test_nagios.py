from nodetraq.tests import *

class TestNagiosController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='nagios', action='index'))
        # Test response...
