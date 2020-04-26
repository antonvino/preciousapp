from logs.models import Day
from logs.models import Hour
from logs.tests.testing_lib import RegularTest

class HourTests(RegularTest):

    # TODO put this in the Day tests 
    #
    def test_hour_summary_page(self):
        """
        Check that user can go to the page and see the 
        return the response
        """
        pass
        # response = self.assert_page_loading("/day")
        # self.assertContains(response, "Day at a glance")