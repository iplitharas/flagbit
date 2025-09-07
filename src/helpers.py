from datetime import datetime, timedelta
from pytz import utc
from src.types import EXP_UNIT_T


def new_expiration_date_from_now(unit: EXP_UNIT_T, value: int) -> datetime:
    match unit:
        case "m":
            return datetime.now(tz=utc) + timedelta(minutes=value)
        case "h":
            return datetime.now(tz=utc) + timedelta(hours=value)
        case "d":
            return datetime.now(tz=utc) + timedelta(days=value)
        case "w":
            return datetime.now(tz=utc) + timedelta(weeks=value)
