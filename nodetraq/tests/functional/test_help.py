from nodetraq.tests import *

class TestHelpController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='help', action='index'))
        # Test response...
