from laboris.util import pick_one_task
from pony import orm
from datetime import datetime

import click

from laboris.ui import task_short


@click.command(name="done")
@click.argument("label", nargs=1)
def done_command(label: str):
    """Mark a task as completed"""
    with orm.db_session:
        db_task = pick_one_task(label)
        if db_task is None:
            return 1

        if len(db_task.events) != 0 and len(db_task.events[-1]) == 1:
            db_task.events[-1].append(datetime.now().timestamp())
        db_task.updatedDate = datetime.now()
        db_task.doneDate = datetime.now()
        db_task.state = "DONE"
        click.echo(f"Marked the task {task_short(db_task)} as completed")
