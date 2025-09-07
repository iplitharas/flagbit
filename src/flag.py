from dataclasses import dataclass, field
from datetime import datetime
from pytz import utc
from uuid import uuid4
from uuid import UUID


@dataclass
class Flag:
    name: str
    value: bool
    desc: str | None = None
    date_created: datetime = field(default_factory=lambda: datetime.now(tz=utc))
    id: UUID = field(default_factory=uuid4)
