from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from laboris.ui import Table, error
from laboris.util import date_parser as date, taskQuery
from pony import orm
from halo import Halo
import click

# __BAR_CHARS__ = ["█", "▉", "▊", "▋", "▌", "▍", "▎", "▏"]
__BAR_CHARS__ = ["█"]
__BAR_WIDTH__ = 120


@click.command(name="gantt")
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
    "-S",
    "--day-start",
    type=int,
    default=0,
    help="Set what out of the day to start the graph at",
)
@click.option(
    "-E",
    "--day-end",
    type=int,
    default=23,
    help="Set what out of the day to end the graph at",
)
@click.argument("query", nargs=-1)
def gantt_command(
    query: Tuple[str, ...],
    start: datetime,
    end: datetime,
    day_start: int,
    day_end: int,
    hidden: bool,
):
    """Generate a graph displaying time spent activly working on every task"""

    if start >= end:
        click.echo(error(f"Start date must be before end date {start} >= {end}"))
        return 1
    elif day_start >= day_end:
        click.echo(
            error(f"Day start hour must be before the end hour {start} >= {end}")
        )
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
        data: Dict[str, Tuple[datetime, List[Tuple[datetime, str]]]] = {}

        multi: Dict[str, bool] = {
            "year": start.year != end.year,
            "month": start.month != end.month,
        }
        fmt = "%b %d %Y" if multi["year"] else ("%b %d" if multi["month"] else "%d")

        current = start
        while current <= end:
            key = current.strftime(fmt)
            data[key] = (current.replace(hour=0, minute=0, second=0, microsecond=0), [])
            keys.append(key)
            current += timedelta(days=1)
        key = end.strftime(fmt)
        if key not in data:
            data[key] = (current.replace(hour=0, minute=0, second=0, microsecond=0), [])
            keys.append(key)

        for task in tasks:
            color = task.color.strip("#")
            for ev in task.events:
                estart = datetime.fromtimestamp(ev[0])
                if estart.strftime(fmt) in keys:
                    data[estart.strftime(fmt)][1].append((estart, color))
                eend = datetime.fromtimestamp(ev[1]) if len(ev) == 2 else datetime.now()
                if eend.strftime(fmt) in keys:
                    data[eend.strftime(fmt)][1].append((eend, color))

        width = click.get_terminal_size()[0] - max(len(x) for x in data.keys()) + 2

        x_axis = " " * int(
            (width - ((day_end - day_start + 1) * 2)) // (day_end - day_start + 1)
        )
        x_axis = x_axis.join(f"{x:<2}" for x in range(day_start, day_end + 1))

        actual_width = len(x_axis)
        conversion = (
            actual_width
            * len(__BAR_CHARS__)
            / timedelta(hours=(day_end - day_start)).total_seconds()
        )

        table = Table()

        color_stack: List[Optional[str]] = [None]
        for key in keys:
            head = data[key][0] + timedelta(hours=day_start)
            events = sorted(data[key][1], key=lambda x: x[0])

            cells: List[Optional[str]] = [None] * (actual_width * len(__BAR_CHARS__))

            iprev = 0
            for ev in events:
                istart = int((ev[0] - head).total_seconds() * conversion)
                if istart < 0:
                    istart = 0
                elif istart >= len(cells):
                    istart = len(cells) - 1
                for i in range(iprev, istart):
                    cells[i] = color_stack[-1]
                iprev = istart
                if len(color_stack) > 1 and color_stack[-1] == ev[1]:
                    color_stack.pop(-1)
                elif len(color_stack) == 1 and color_stack[0] == ev[1]:
                    color_stack.pop(-1)
                else:
                    color_stack.append(ev[1])

            day: List[Tuple[str, Optional[str], Optional[str]]] = []
            for i in range(actual_width):
                block = cells[i * len(__BAR_CHARS__) : (i + 1) * len(__BAR_CHARS__)]
                day.append(
                    (
                        __BAR_CHARS__[
                            len(__BAR_CHARS__) - sum(1 for x in block if x == block[0])
                        ],
                        block[0],
                        block[-1],
                    )
                )

            row = ""
            for ch, fg, bg in day:
                # if fg and bg:
                #     row += click.style(
                #         ch,
                #         fg=tuple(int(fg[i : i + 2], 16) for i in (0, 2, 4)),
                #         bg=tuple(int(bg[i : i + 2], 16) for i in (0, 2, 4)),
                #     )
                # elif bg:
                #     row += click.style(
                #         ch,
                #         fg="black",
                #         bg=tuple(int(bg[i : i + 2], 16) for i in (0, 2, 4)),
                #     )
                # elif fg:
                #     row += click.style(
                #         ch,
                #         fg=tuple(int(fg[i : i + 2], 16) for i in (0, 2, 4)),
                #         bg="black",
                #     )
                # else:
                #     row += click.style(" ", bg="black")
                if fg and bg:
                    row += click.style(
                        ch,
                        fg=tuple(int(fg[i : i + 2], 16) for i in (0, 2, 4)),
                        bg=tuple(int(bg[i : i + 2], 16) for i in (0, 2, 4)),
                    )
                elif bg:
                    row += click.style(
                        ch,
                        bg=tuple(int(bg[i : i + 2], 16) for i in (0, 2, 4)),
                    )
                elif fg:
                    row += click.style(
                        ch,
                        fg=tuple(int(fg[i : i + 2], 16) for i in (0, 2, 4)),
                    )
                else:
                    row += click.style(" ")

            table.append([click.style(key, bold=True), row])

        table.append(["", x_axis])

        spinner.stop()

        click.echo(table.format())
