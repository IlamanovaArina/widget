from datetime import datetime

import pytest

@pytest.fixture
def date():
    today_date = datetime.datetime.now().day()
    return today_date