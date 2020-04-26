from logs.models import Day
from logs.models import Hour
from logs.tests.testing_lib import RegularTest

class DayTests(RegularTest):

    def test_week_summary_page(self):
        """
        Check that user can go to the page and see the 
        return the response
        """
        response = self.assert_page_loading("/week")
        self.assertContains(response, "Week at a glance")