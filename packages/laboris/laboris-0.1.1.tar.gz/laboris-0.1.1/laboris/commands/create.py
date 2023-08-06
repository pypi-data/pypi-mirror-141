from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional, Tuple
from pony import orm
import click

from laboris.model import Tag, Task
from laboris.ui import error, task_short
from laboris.util import date_parser as date, duration_parser as duration


def parse_goal(string: str) -> Tuple[timedelta, timedelta]:
    return duration(string.split("/", 1)[0]), duration(string.split("/", 1)[-1])


@click.command(name="create")
@click.option("-d", "--due", type=date, help="Set the due date of the task")
@click.option(
    "-P", "--priority", type=int, default=5, help="Set a priority for the task"
)
@click.option(
    "-p", "--parent", type=str, multiple=True, help="Specify any parent tasks"
)
@click.option(
    "-t", "--tag", type=str, multiple=True, help="Specify any tags for the task"
)
@click.option(
    "-g",
    "--goal",
    type=(duration, duration),
    help="Set a goal to work on the task",
)
@click.option(
    "-H",
    "--hidden/--no-hidden",
    default=False,
    help="Mark that task as hidden",
)
@click.argument("label", nargs=-1)
def create_command(
    label: Tuple[str, ...],
    due: Optional[datetime],
    priority: int,
    parent: Tuple[str, ...],
    tag: Tuple[str, ...],
    goal: Optional[Tuple[timedelta, timedelta]],
    hidden: bool,
):
    """Create a new task"""
    with orm.db_session:
        db_tags = list(Task.select())
        db_tasks = list(Task.select(lambda t: t.state == "OPEN"))

        arg_label = " ".join(
            x for x in label if x[0] not in ("+", "@") and ":" not in x
        )
        arg_tag = list(tag) + [x[1:] for x in label if x[0] == "@"]
        arg_parent = list(parent) + [x[1:] for x in label if x[0] == "+"]
        metadata = {x.split(":", 1)[0]: x.split(":", 1)[-1] for x in label if ":" in x}

        def parse_metadata(keys: List[str], func: Callable, default: Any) -> Any:
            for k in keys:
                if k in metadata:
                    return func(metadata[k])
            return default

        due = parse_metadata(["due", "dueDate"], date, due)
        priority = parse_metadata(["p", "pri", "priority"], int, priority)
        goal = parse_metadata(["goal", "target"], parse_goal, goal)

        tags = [
            next((y for y in db_tags if x.lower() == y.label.lower()), x)
            if type(x) == str
            else x
            for x in arg_tag
        ]
        tags = [Tag(label=x) if type(x) == str else x for x in tags]

        parents = [
            next(
                (
                    y
                    for y in db_tasks
                    if x.lower() == y.label.lower() or str(y.uuid).startswith(x)
                ),
                x,
            )
            if type(x) == str
            else x
            for x in arg_parent
        ]

        if any([type(x) == str for x in parents]):
            click.echo(
                error(
                    f"Not all parent tasks were found, missing {', '.join([repr(x) for x in parents if type(x) == str])}"
                )
            )
            return 1

        task = Task(
            label=arg_label,
            priority=priority,
            dueDate=due,
            tags=tags,
            goalDuration=goal[0] if goal else None,
            goalPeriod=goal[1] if goal else None,
            parents=parents,
            hidden=hidden,
        )

        click.echo(f"Created new task {task_short(task)}")
