import time as time_module
import datetime
from typing import Optional


def now() -> datetime.datetime:
    utc = datetime.timezone.utc
    return datetime.datetime.now(tz=utc)


def datetime_to_epoch(date: Optional[datetime.datetime]) -> Optional[int]:
    if date is None:
        return None
    if isinstance(date, datetime.date) and not isinstance(date, datetime.datetime):
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
    return int(date.timestamp())


def epoch_now() -> int:
    return int(time_module.time())


def date_code(year: int, month: int, day: int) -> str:
    return f'{str(year)[-2:]}{month:02d}{day:02d}'

