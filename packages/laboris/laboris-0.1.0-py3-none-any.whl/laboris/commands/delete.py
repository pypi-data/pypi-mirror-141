from laboris.util import pick_one_task
from pony import orm

import click

from laboris.model import Task
from laboris.ui import task_short


@click.command(name="delete")
@click.argument("label", nargs=1)
def delete_command(
    label: str,
):
    """Delete an existing task"""
    with orm.db_session:
        db_task = pick_one_task(label)
        if db_task is None:
            return 1
        elif click.confirm(f"Do you want to delete {task_short(db_task)}?", abort=True):
            rep = task_short(db_task)
            db_task.delete()
            click.echo(f"Deleted the task {rep}")
