from nodetraq.tests import *

class TestMenusController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='menus', action='index'))
        # Test response...
