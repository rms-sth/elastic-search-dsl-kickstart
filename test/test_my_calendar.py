# import unittest
# from unittest.mock import patch

# from requests.exceptions import Timeout

# from my_calendar import get_holidays


# class TestCalendar(unittest.TestCase):
#     @patch("my_calendar.requests")
#     def test_get_holidays_timeout(self, mock_requests):
#         mock_requests.get.side_effect = Timeout
#         with self.assertRaises(Timeout):
#             get_holidays()
#             mock_requests.get.assert_called_once()


# if __name__ == "__main__":
#     unittest.main()


# import unittest
# from unittest.mock import patch

# from requests.exceptions import Timeout

# from my_calendar import get_holidays


# class TestCalendar(unittest.TestCase):
#     def test_get_holidays_timeout(self):
#         with patch("my_calendar.requests") as mock_requests:
#             mock_requests.get.side_effect = Timeout
#             with self.assertRaises(Timeout):
#                 get_holidays()
#                 mock_requests.get.assert_called_once()


# if __name__ == "__main__":
#     unittest.main()


import unittest
from unittest.mock import patch

from my_calendar import get_holidays, requests


class TestCalendar(unittest.TestCase):
    @patch.object(requests, "get", side_effect=requests.exceptions.Timeout)
    def test_get_holidays_timeout(self, mock_requests):
        with self.assertRaises(requests.exceptions.Timeout):
            get_holidays()


if __name__ == "__main__":
    unittest.main()
