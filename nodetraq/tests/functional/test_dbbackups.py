from nodetraq.tests import *

class TestDbbackupsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dbbackups', action='index'))
        # Test response...
