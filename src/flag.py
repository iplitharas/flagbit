from dataclasses import dataclass, field
from datetime import datetime
from pytz import utc


@dataclass
class Flag:
    name: str
    value: bool
    desc: str | None = None
    date_created: datetime = field(default=datetime.now(tz=utc))
