from nodetraq.tests import *

class TestActivityController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='activity', action='index'))
        # Test response...
