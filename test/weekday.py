from unittest.mock import patch

import my_calendar

with patch("my_calendar.is_weekday"):
    print(my_calendar.is_weekday())


from my_calendar import is_weekday
from unittest.mock import patch

with patch("my_calendar.is_weekday"):
    print(is_weekday())


from unittest.mock import patch
from my_calendar import is_weekday

with patch("__main__.is_weekday"):
    print(is_weekday())