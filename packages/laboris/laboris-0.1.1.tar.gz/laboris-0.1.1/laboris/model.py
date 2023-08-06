from typing import Dict
import uuid
from hashlib import md5
from datetime import datetime, timedelta
from pony.orm import *

db = Database()


class Tag(db.Entity):
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    label = Required(str)
    tasks = Set("Task")


class Task(db.Entity):
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    state = Required(str, default="OPEN")
    hidden = Required(bool, default=False)
    label = Required(str)
    priority = Required(int, default=5)
    tags = Set("Tag")
    parents = Set("Task", reverse="children")
    children = Set("Task", reverse="parents")
    dueDate = Optional(datetime)
    goalDuration = Optional(timedelta)
    goalPeriod = Optional(timedelta)
    createdDate = Required(datetime, default=datetime.now())
    updatedDate = Required(datetime, default=datetime.now())
    doneDate = Optional(datetime)
    events = Required(Json, default=[])

    @property
    def shortUuid(self) -> str:
        return str(self.uuid).split("-", 1)[0]

    @property
    def active(self) -> bool:
        return len(self.events) != 0 and len(self.events[-1]) == 1

    @property
    def urgency(self) -> float:
        urg = 5 - self.priority
        urg += 0.1 * (datetime.now() - self.createdDate).total_seconds() / 86400
        if self.active:
            urg += 2.0
        if self.dueDate:
            urg += 8.0 * (
                (datetime.now() - self.createdDate) / (self.dueDate - self.createdDate)
            )

        if self.goalDuration and self.goalPeriod:
            time = 0.0
            now = datetime.now().timestamp()
            P = self.goalPeriod.total_seconds()
            for event in [x for x in self.events if len(x) == 1 or x[1] > (now - P)]:
                a = max(event[0], now - P) - now
                b = (event[1] if len(event) == 2 else now) - now
                t = (b - a) * (2 * P + b + a) / (2 * P)
                time += t

            urg += 8.0 * max(1 - (time / self.goalDuration.total_seconds()), 0)
        return urg

    @property
    def priorityColor(self) -> Dict:
        pri = self.priority
        if pri <= 0:
            return {"fg": "red", "bold": True}
        elif pri <= 1:
            return {"fg": "red"}
        elif pri <= 2:
            return {"fg": "yellow"}
        elif pri <= 3:
            return {"fg": "green"}
        elif pri <= 4:
            return {"fg": "blue"}
        return {}

    @property
    def urgencyColor(self) -> Dict:
        urg = self.urgency
        if urg >= 10.0:
            return {"fg": "red", "underline": True, "bold": True}
        elif urg >= 9.0:
            return {"fg": "red", "bold": True}
        elif urg >= 8.0:
            return {"fg": "red"}
        elif urg >= 6.0:
            return {"fg": "yellow"}
        elif urg >= 4.0:
            return {"fg": "green"}
        elif urg >= 1.0:
            return {"fg": "blue"}
        return {}

    @property
    def color(self) -> str:
        return f"#{int(md5((self.label + self.createdDate.isoformat()).encode('utf-8')).hexdigest(), 16) % 0xFFFFFF:06X}"
