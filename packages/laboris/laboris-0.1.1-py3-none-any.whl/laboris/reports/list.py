from datetime import datetime
from typing import Tuple
from laboris.util import taskQuery
from pony import orm
import humanize
import click

from laboris.ui import Table


@click.command(name="list")
@click.option("--csv/--no-csv", default=False, help="Format output as a CSV")
@click.option(
    "--done/--no-done", default=False, help="Include completed tasks in the results"
)
@click.option(
    "--hidden/--no-hidden", default=False, help="Include hidden tasks in the results"
)
@click.argument("query", nargs=-1)
def list_command(query: Tuple[str, ...], csv: bool, done: bool, hidden: bool):
    """List all current tasks in an easy to read table"""
    with orm.db_session:
        db_query = taskQuery(
            lambda t: (hidden or t.hidden == False) and (done or t.state == "OPEN"),
            *query,
        )
        db_tasks = sorted(list(db_query), key=lambda x: x.urgency, reverse=True)

        table = Table(
            header=["A", "UUID", "P", "Due", "Tags", "Projects", "Label", "Urg"],
            header_style={"underline": True, "bold": True},
            align=["<", "<", ">", ">", "<", "<", "<", ">"],
        )

        for t in db_tasks:
            table.append(
                [
                    click.style("●" if t.active else "", fg="green", bold=True),
                    click.style(t.shortUuid, fg="bright_black"),
                    click.style(t.priority, **t.priorityColor),
                    click.style(
                        f"{'-' if t.dueDate < datetime.now() else ''}{humanize.naturaldelta(t.dueDate - datetime.now())}"
                        if t.dueDate is not None
                        else "",
                        fg="magenta",
                    ),
                    click.style(
                        ("@" if len(t.tags) != 0 else "")
                        + " @".join([x.label for x in t.tags]),
                        fg="yellow",
                    ),
                    click.style(
                        ("+" if len(t.parents) != 0 else "")
                        + " +".join([x.label for x in t.parents]),
                        fg="blue",
                    ),
                    t.label,
                    click.style(f"{t.urgency:3.1f}", **t.urgencyColor),
                ]
            )

        click.echo(table.format(csv))
