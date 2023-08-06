from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from laboris.ui import Table, error
from laboris.util import date_parser as date, taskQuery
from pony import orm
from halo import Halo
import click

__BAR_CHAR__ = "■"
__BAR_WIDTH__ = 40


@click.command(name="graph")
@click.option(
    "--hidden/--no-hidden", default=False, help="Include hidden tasks in the results"
)
@click.option(
    "-s",
    "--start",
    type=date,
    default=datetime.now() - timedelta(days=7),
    help="Set the starting date for the report",
)
@click.option(
    "-e",
    "--end",
    type=date,
    default=datetime.now() + timedelta(hours=1),
    help="Set the ending date for the report",
)
@click.option(
    "-p",
    "--period",
    default="day",
    type=click.Choice(["year", "month", "week", "day"], case_sensitive=False),
    help="Set the bin size for the graph",
)
@click.argument("query", nargs=-1)
def graph_command(
    query: Tuple[str, ...], start: datetime, end: datetime, period: str, hidden: bool
):
    """Generate a graph displaying the number of created/open/closed tasks over time"""

    if start >= end:
        click.echo(error(f"Start date must be before end date {start} >= {end}"))
        return 1

    with orm.db_session:
        spinner = Halo(text="Constructing report")
        spinner.start()
        tasks = list(
            taskQuery(
                lambda t: (hidden or t.hidden == False)
                and (t.createdDate >= start or t.doneDate >= start)
                and (t.createdDate <= end or t.doneDate <= end),
                *query,
            )
        )

        keys: List[str] = []
        data: Dict[str, List[int]] = {}

        multi: Dict[str, bool] = {
            "year": start.year != end.year,
            "month": start.month != end.month,
        }
        if period == "year":
            diff = timedelta(days=365)
        elif period == "month":
            diff = timedelta(days=30)
        elif period == "week":
            diff = timedelta(days=7)
        else:
            diff = timedelta(days=1)

        if period == "year":
            fmt = "%Y"
        elif period == "month":
            fmt = "%b %Y" if multi["year"] else "%b"
        elif period == "week":
            fmt = "%Y W%W" if multi["year"] else "W%W"
        else:
            fmt = "%b %d %Y" if multi["year"] else ("%b %d" if multi["month"] else "%d")

        current = start
        while current <= end:
            key = current.strftime(fmt)
            data[key] = [0, 0, 0, 0]
            keys.append(key)
            current += diff
        key = end.strftime(fmt)
        if key not in data:
            data[key] = [0, 0, 0, 0]
            keys.append(key)

        for task in tasks:
            tstart = task.createdDate if task.createdDate >= start else start
            tend = task.doneDate if task.doneDate else end

            istart = keys.index(tstart.strftime(fmt))
            iend = keys.index(tend.strftime(fmt))

            data[keys[istart]][0] += 1
            if task.doneDate is not None:
                data[keys[iend]][3] += 1

            if istart != iend:
                for k in keys[istart + 1 : iend + 1]:
                    if any(
                        [
                            datetime.fromtimestamp(x[0]).strftime(fmt) == k
                            for x in task.events
                        ]
                    ):
                        data[k][2] += 1
                    else:
                        data[k][1] += 1

        maximum_sum = max([sum(x) for x in data.values()])

        def bar(new: int, open: int, active: int, closed: int) -> str:
            sum = new + open + closed + active
            if sum == 0:
                return ""
            size = int(__BAR_WIDTH__ * sum / maximum_sum)
            ret = ""
            for (val, fg) in [
                (new, "yellow"),
                (open, "bright_black"),
                (active, "blue"),
                (closed, "green"),
            ]:
                if sum == 0:
                    break
                comp = int(size * val / sum)
                ret += click.style(__BAR_CHAR__ * comp, fg=fg)
                size -= comp
                sum -= val
            return ret

        table = Table(align=[">", ">", ">", ">", ">", "<"])
        for key in keys:
            row = data[key]
            table.append(
                [
                    click.style(key, bold=True),
                    click.style(str(row[0]), fg="yellow", bold=True),
                    click.style(str(row[1]), fg="bright_black", bold=True),
                    click.style(str(row[2]), fg="blue", bold=True),
                    click.style(str(row[3]), fg="green", bold=True),
                    bar(*row),
                ]
            )

        spinner.stop()

        click.echo(table.format())
