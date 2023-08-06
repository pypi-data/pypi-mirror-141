from datetime import datetime, timedelta
from typing import Callable, List, Optional, Union
from pony import orm
import click
import re
import isodate
from dateutil import parser

from laboris.model import Tag, Task
from laboris.ui import error

__DURATION_PARSER__ = re.compile(
    r"((?P<year>[0-9]+)y)?((?P<month>[0-9]+)M)?((?P<week>[0-9]+)w)?((?P<day>[0-9]+)d)?((?P<hour>[0-9]+)h)?((?P<minute>[0-9]+)m)?((?P<second>[0-9]+)s)?"
)
__RELATIVE_DURATION_PARSER__ = re.compile(
    r"(?P<sign>[+-])?((?P<year>[0-9]+)y)?((?P<month>[0-9]+)M)?((?P<week>[0-9]+)w)?((?P<day>[0-9]+)d)?((?P<hour>[0-9]+)h)?((?P<minute>[0-9]+)m)?((?P<second>[0-9]+)s)?"
)
__CONDITION_REGEX__ = re.compile(
    r"(?P<lhs>[^!~=<>]+)(?P<op>[~~=<>]{1,2})(?P<rhs>[^!~=<>]+)"
)


def date_parser(string: Union[str, datetime]) -> datetime:
    if isinstance(string, datetime):
        return string
    match = re.match(__RELATIVE_DURATION_PARSER__, string)
    if match is None or not match.group(0):
        return parser.parse(string)
    else:
        now = datetime.now()
        sign = -1 if match.group("sign") == "-" else 1
        if match.group("year"):
            now += timedelta(days=sign * 365 * int(match.group("year")))
        if match.group("month"):
            now += timedelta(days=sign * 30 * int(match.group("month")))
        if match.group("week"):
            now += timedelta(days=sign * 7 * int(match.group("week")))
        if match.group("day"):
            now += timedelta(days=sign * int(match.group("day")))
        if match.group("hour"):
            now += timedelta(hours=sign * int(match.group("hour")))
        if match.group("minute"):
            now += timedelta(minutes=sign * int(match.group("minute")))
        if match.group("second"):
            now += timedelta(seconds=sign * int(match.group("second")))
        return now


def duration_parser(string: Union[str, timedelta]) -> timedelta:
    if isinstance(string, timedelta):
        return string
    match = re.match(__DURATION_PARSER__, string)
    if match is None or not match.group(0):
        return isodate.parse_duration(string)
    else:
        now = timedelta()
        if match.group("year"):
            now += timedelta(days=365 * int(match.group("year")))
        if match.group("month"):
            now += timedelta(days=30 * int(match.group("month")))
        if match.group("week"):
            now += timedelta(days=7 * int(match.group("week")))
        if match.group("day"):
            now += timedelta(days=int(match.group("day")))
        if match.group("hour"):
            now += timedelta(hours=int(match.group("hour")))
        if match.group("minute"):
            now += timedelta(minutes=int(match.group("minute")))
        if match.group("second"):
            now += timedelta(seconds=int(match.group("second")))
        return now


def pick_one_task(label: str, state: List[str] = ["OPEN"]) -> Optional[Task]:
    tasks = list(
        Task.select(lambda t: t.state in state and t.label.lower().startswith(label))
    )

    if len(tasks) == 1:
        return tasks[0]

    tasks = list(Task.select(lambda t: t.state in state))
    tasks = [x for x in tasks if str(x.uuid).startswith(label)]

    if len(tasks) == 0:
        click.echo(error(f"Faild to find a task with the label {repr(label)}"))
        return None
    elif len(tasks) != 1:
        click.echo(error(f"Found multiple tasks matching the label {repr(label)}"))
        return None
    return tasks[0]


def taskQuery(init: Callable, *args):
    query = Task.select(init)

    for arg in args:
        if type(arg) != str:
            query = query.where(arg)
        elif arg[0] == "@":
            tag = Tag.select(lambda x: x.label == arg[1:]).get()
            query = query.where(lambda t: tag in t.tags)
        elif arg[0] == "+":
            task = Task.select(lambda x: x.label == arg[1:]).get()
            query = query.where(lambda t: task in t.parents)
        elif arg[0] == "_":
            task = Task.select(lambda x: x.label == arg[1:]).get()
            query = query.where(lambda t: task in t.children)
        else:
            m = re.match(__CONDITION_REGEX__, arg)
            if m is None:
                query = query.where(lambda t: arg in t.label)
                continue

            lhs = m.group("lhs")
            op = m.group("op")
            rhs = m.group("rhs")

            if op == "~=":
                op = "in"

            lhs_key = False
            if lhs in (
                "state",
                "hidden",
                "label",
                "priority",
                "dueDate",
                "goalDuration",
                "goalPeriod",
                "createdDate",
                "updatedDate",
                "doneDate",
            ):
                lhs_key = True

            key = lhs if lhs_key else rhs
            value = rhs if lhs_key else lhs

            if key in (
                "dueDate",
                "createdDate",
                "updatedDate",
                "doneDate",
            ):
                value = date_parser(value)
            elif key in ("priority",):
                value = int(value)
            elif key in ("goalDuration", "goalPeriod"):
                value = duration_parser(value)
            elif key in ("hidden"):
                value = True if value.lower() == "true" else False

            query = query.where(
                f"{'t.' + key if lhs_key else 'x'} {op} {'x' if lhs_key else 't.' + key}",
                {"x": value},
            )

    return query
