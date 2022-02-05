from datetime import datetime, timezone
from typing import Union


def _is_valid_date(date: Union[str, datetime]) -> bool:
    """
    Return True iif date is in ISO format
    """

    if isinstance(date, datetime):
        valid = True
    elif isinstance(date, str):
        iso_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        try:
            _ = datetime.strptime(date, iso_format)  # fails if not ISO format
            valid = True
        except ValueError:
            valid = False
    else:
        valid = False

    return valid
