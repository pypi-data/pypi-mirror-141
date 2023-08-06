from datetime import datetime, timedelta


def ms_to_datetime(millis: int) -> datetime:
    """
    Converts an integer value that represents milliseconds since the UNIX epoch to a datetime object.

    Parameters:
        millis: milliseconds since the UNIX epoch

    Returns:
        A datetime object
    """

    base_datetime = datetime(1970, 1, 1)
    utc_time = base_datetime + timedelta(milliseconds=millis)

    return utc_time


def datetime_to_ms(dt: datetime) -> int:
    """
    Converts a datetime object to an integer value that represents milliseconds since the UNIX epoch.

    Parameters:
        dt (datetime): datetime object

    Returns:
        An integer value that represents milliseconds since the UNIX epoch
    """

    epoch = datetime.utcfromtimestamp(0)
    ms = (dt - epoch).total_seconds() * 1000.0
    return ms


# def timestamp_to_datetime(timestamp):
#     """ """
#     tmp = timestamp.str.split("T", expand=True)

#     date = tmp[0].str.split("-", expand=True)
#     date.columns = ["year", "month", "day"]

#     time = tmp[1].str.split(":", expand=True)
#     time.columns = ["hour", "minutes", "seconds", "zeros"]

#     df = pd.concat([date, time], axis=1)
#     df = df.drop(columns=["seconds", "zeros"])
#     df = df["year"] + df["month"] + df["day"] + df["hour"] + df["minutes"]
#     df = pd.to_datetime(df, format="%Y%m%d%H%M")

#     return df
