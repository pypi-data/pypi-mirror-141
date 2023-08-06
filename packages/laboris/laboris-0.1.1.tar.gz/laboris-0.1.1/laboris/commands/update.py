from typing import Any, Callable, List, Tuple, Optional
from pony import orm
from datetime import datetime, timedelta
import click

from laboris.model import Tag, Task
from laboris.ui import error, task_short
from laboris.util import date_parser as date, duration_parser as duration, pick_one_task


def parse_goal(string: str) -> Tuple[timedelta, timedelta]:
    return duration(string.split("/", 1)[0]), duration(string.split("/", 1)[-1])


@click.command(name="update")
@click.option("-d", "--due", type=date, help="Set the due date of the task")
@click.option("-P", "--priority", type=int, help="Set a priority for the task")
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
    help="Mark that task as hidden",
)
@click.option(
    "-l", "--label", "new_label", type=str, multiple=True, help="New label for the task"
)
@click.argument("label", nargs=1)
@click.argument("args", nargs=-1)
def update_command(
    label: str,
    due: Optional[datetime],
    priority: Optional[int],
    parent: Tuple[str, ...],
    tag: Tuple[str, ...],
    goal: Optional[Tuple[timedelta, timedelta]],
    hidden: Optional[bool],
    new_label: Tuple[str, ...],
    args: Tuple[str, ...],
):
    """Update an exiting task"""
    with orm.db_session:
        task = pick_one_task(label)
        if task is None:
            return 1

        db_tags = list(Tag.select())
        db_tasks = list(Task.select(lambda t: t.state == "OPEN"))

        arg_tag = list(tag) + [x[1:] for x in args if x[0] == "@"]
        arg_parent = list(parent) + [x[1:] for x in args if x[0] == "+"]
        metadata = {x.split(":", 1)[0]: x.split(":", 1)[-1] for x in args if ":" in x}

        def parse_metadata(keys: List[str], func: Callable, default: Any) -> Any:
            for k in keys:
                if k in metadata:
                    return func(metadata[k])
            return default

        due = parse_metadata(["due", "dueDate"], date, due)
        priority = parse_metadata(["p", "pri", "priority"], int, priority)
        goal = parse_metadata(["goal", "target"], parse_goal, goal)

        if len(arg_tag) != 0:
            tags = [
                next((y for y in db_tags if x.lower() == y.label.lower()), x)
                if type(x) == str
                else x
                for x in arg_tag
            ]
            task.tags = [Tag(label=x) if type(x) == str else x for x in tags]

        if len(arg_parent) != 0:
            parents = [
                next((y for y in db_tasks if x.lower() == y.label.lower()), x)
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

            task.parents = parents

        if due is not None:
            task.dueDate = due

        if priority is not None:
            task.priority = priority

        if goal is not None:
            task.goalDuration = goal[0]
            task.goalPeriod = goal[1]

        if hidden is not None:
            task.hidden = hidden

        if len(new_label) != 0:
            task.label = " ".join(new_label)

        task.updatedDate = datetime.now()
        click.echo(f"Updated task {task_short(task)}")
