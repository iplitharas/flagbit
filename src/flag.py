from dataclasses import dataclass, field
from datetime import datetime
from pytz import utc


@dataclass(frozen=True)
class Flag:
    name: str
    date_created: datetime = field(default=datetime.now(tz=utc))
