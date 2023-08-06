from typing import Optional
from laboris.util import date_parser as date, pick_one_task
from pony import orm
from datetime import datetime

import click

from laboris.ui import error, task_short


@click.command(name="stop", context_settings={"ignore_unknown_options": True})
@click.argument("label", nargs=1)
@click.argument("date", type=date, required=False)
def stop_command(label: str, date: Optional[datetime]):
    """Stop tracking activity on a task"""
    with orm.db_session:
        db_task = pick_one_task(label)
        if db_task is None:
            return 1
        elif len(db_task.events) == 0 or len(db_task.events[-1]) != 1:
            click.echo(
                error(f"The task {task_short(db_task)}")
                + error(" is not currently active")
            )
            return 1
        db_task.events[-1].append(
            date.timestamp() if date else datetime.now().timestamp()
        )
        db_task.updatedDate = datetime.now()
        click.echo(f"Stopped progress on {task_short(db_task)}")
