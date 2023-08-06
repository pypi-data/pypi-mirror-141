from datetime import datetime, timedelta
from laboris.ui import Table
from laboris.util import pick_one_task
from pony import orm
import humanize

import click


@click.command(name="detail")
@click.option("--csv/--no-csv", default=False, help="Format output as a CSV")
@click.argument("label", nargs=1)
def detail_command(label: str, csv: bool):
    """List details of a specific task"""
    with orm.db_session:
        db_task = pick_one_task(label)
        if db_task is None:
            return 1

        table = Table(
            header=["Key", "Value"],
            header_style={"underline": True, "bold": True},
            align=[">", "<"],
        )
        table.append(
            [
                click.style("UUID", bold=True),
                click.style(str(db_task.uuid), fg="bright_black"),
            ]
        )
        table.append(
            [click.style("State", bold=True), click.style(db_task.state, fg="cyan")]
        )
        table.append([click.style("Label", bold=True), db_task.label])
        table.append(
            [
                click.style("Priority", bold=True),
                click.style(db_task.priority, **db_task.priorityColor),
            ]
        )

        tag_table = Table(header=["UUID", "Label"], header_style={"bold": True})
        for tag in db_task.tags:
            tag_table.append(
                [
                    click.style(tag.uuid, fg="bright_black"),
                    click.style(tag.label, fg="yellow"),
                ]
            )
        table.append(
            [
                click.style("Tags", bold=True),
                tag_table.format() if len(db_task.tags) != 0 else "",
            ]
        )

        parent_table = Table(header=["State", "UUID", "Label"], header_style={"bold": True})
        for task in db_task.parents:
            parent_table.append(
                [
                    click.style(task.state, fg="cyan"),
                    click.style(task.uuid, fg="bright_black"),
                    click.style(task.label, fg="blue"),
                ]
            )
        table.append(
            [
                click.style("Parent Tasks", bold=True),
                parent_table.format() if len(db_task.parents) else "",
            ]
        )

        child_table = Table(header=["State", "UUID", "Label"], header_style={"bold": True})
        for task in db_task.children:
            child_table.append(
                [
                    click.style(task.state, fg="cyan"),
                    click.style(task.uuid, fg="bright_black"),
                    click.style(task.label, fg="blue"),
                ]
            )
        table.append(
            [
                click.style("Child Tasks", bold=True),
                child_table.format() if len(db_task.children) else "",
            ]
        )

        table.append(
            [
                click.style("Due Date", bold=True),
                click.style(
                    f"{db_task.dueDate:%c}" if db_task.dueDate else "",
                    fg="magenta",
                ),
            ]
        )

        table.append(
            [
                click.style("Goal", bold=True),
                click.style(
                    f"{humanize.naturaldelta(db_task.goalDuration)} / {humanize.naturaldelta(db_task.goalPeriod)}"
                    if db_task.goalDuration and db_task.goalPeriod
                    else "",
                    fg="magenta",
                ),
            ]
        )

        table.append(
            [
                click.style("Created Date", bold=True),
                click.style(f"{db_task.createdDate:%c}", fg="yellow"),
            ]
        )
        table.append(
            [
                click.style("Updated Date", bold=True),
                click.style(f"{db_task.updatedDate:%c}", fg="yellow"),
            ]
        )
        table.append(
            [
                click.style("Done Date", bold=True),
                click.style(
                    f"{db_task.doneDate:%c}" if db_task.doneDate else "", fg="yellow"
                ),
            ]
        )

        event_table = Table(
            header=["Start", "Stop", "Duration"],
            header_style={"bold": True},
            align=["<", "<", "<"],
        )
        for event in db_task.events:
            ev = [datetime.fromtimestamp(x) for x in event]
            if len(ev) == 2:
                event_table.append(
                    [
                        click.style(f"{ev[0]:%c}", fg="yellow"),
                        click.style(f"{ev[1]:%c}", fg="yellow"),
                        click.style(f"{ev[1] - ev[0]:}", fg="green"),
                    ]
                )
            else:
                event_table.append(
                    [
                        click.style(f"{ev[0]:%c}", fg="yellow"),
                        click.style("NOW", fg="yellow", bold=True),
                        click.style(f"{datetime.now() - ev[0]}", fg="green"),
                    ]
                )

        if len(db_task.events) != 0:
            total = timedelta()
            for event in db_task.events:
                if len(event) == 2:
                    total += timedelta(seconds=event[1] - event[0])
                else:
                    total += timedelta(seconds=datetime.now().timestamp() - event[0])
            event_table.append(["", "", click.style(f"{total}", fg="green", bold=True)])

        table.append(
            [
                click.style("Events", bold=True),
                event_table.format() if len(db_task.events) else "",
            ]
        )

        table.append(
            [
                click.style("Urgency", bold=True),
                click.style(f"{db_task.urgency:4.1f}", **db_task.urgencyColor),
            ]
        )

        click.echo(table.format(csv))
