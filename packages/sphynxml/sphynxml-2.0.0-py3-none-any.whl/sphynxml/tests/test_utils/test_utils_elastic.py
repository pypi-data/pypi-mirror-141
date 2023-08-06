from datetime import datetime

from sphynxml.utils._elasticsearch import datetime_to_ms, ms_to_datetime


def test_ms_to_datetime_unix_epoch():
    """
    | GIVEN   An integer variable equal to zero (milliseconds since UNIX epoch)
    | WHEN    Passing the integer to ms_to_datetime()
    | THEN    A datetime object is return with date equal to 1/1/1970
    """

    ms = 0
    dt_res = ms_to_datetime(ms)

    assert dt_res == datetime(1970, 1, 1)


def test_ms_to_datetime_current():
    """
    | GIVEN   A integer representing milliseconds since UNIX epoch
    | WHEN    Passing the integer to ms_to_datetime()
    | THEN    A datetime object is return with the respective date
    """
    ms = 1642754132924
    ms_time = ms_to_datetime(ms).strftime("%Y-%m-%d %H:%M:%S")
    true_time = datetime(2022, 1, 21, 8, 35, 32).strftime("%Y-%m-%d %H:%M:%S")

    assert ms_time == true_time


def test_datetime_to_ms_unix_epoch():
    """
    | GIVEN   A datetime initialized to 1/1/1970
    | WHEN    Passing the datetime to datetime_to_ms()
    | THEN    An integer is retured initialized to 0, representing the start of UNIX epoch
    """

    date = datetime(1970, 1, 1)
    ms_res = datetime_to_ms(date)

    assert ms_res == 0


def test_datetime_to_ms_current():
    """
    | GIVEN   A datetime object
    | WHEN    Passing the datetime to datetime_to_ms()
    | THEN    An integer is retured, representing milliseconds since UNIX epoch
    """

    ms_time = datetime_to_ms(datetime(2022, 1, 21, 8, 35, 32))

    assert ms_time == 1642754132000
