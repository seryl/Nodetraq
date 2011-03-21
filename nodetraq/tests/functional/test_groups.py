from nodetraq.tests import *

class TestGroupsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='groups', action='index'))
        # Test response...
