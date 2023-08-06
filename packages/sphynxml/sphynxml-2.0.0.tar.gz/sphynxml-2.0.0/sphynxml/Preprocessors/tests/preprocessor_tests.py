import re


def check_timestamp_format(timestamp: str) -> bool:
    """Checks if the format of the timestamp can be handled by the
    expand_timestamp() function.

        Parameters:
            timestamp (str): the timestamp to check

        Return:
            True if the format can be handled, else False
    """
    r = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.000*")

    if r.match(timestamp) is None:
        return False

    return True
