from os import path
from typing import Any
import pkg_resources
import click

from laboris.reports.detail import detail_command
from laboris.commands.done import done_command
from laboris.commands.start import start_command
from laboris.commands.stop import stop_command
from laboris.commands.create import create_command
from laboris.commands.delete import delete_command
from laboris.commands.update import update_command
from laboris.reports.gantt import gantt_command
from laboris.reports.graph import graph_command
from laboris.reports.list import list_command
from laboris.model import db

__version__ = pkg_resources.get_distribution("laboris").version


@click.group(name="laboris")
@click.option(
    "-v", "--verbose", count=True, help="Increase the verbosity of log messages."
)
@click.version_option(__version__)
def main(verbose: int):
    """A personal task manager and time tracker."""

    db.bind(
        provider="sqlite",
        filename=path.join(click.get_app_dir("laboris"), "database.sqlite"),
        create_db=True,
    )
    db.generate_mapping(create_tables=True)


# Create

main.add_command(create_command)

# Read

main.add_command(detail_command)
main.add_command(list_command)
main.add_command(graph_command)
main.add_command(gantt_command)

# Update

main.add_command(done_command)
main.add_command(start_command)
main.add_command(stop_command)
main.add_command(update_command)

# Delete

main.add_command(delete_command)


if __name__ == "__main__":
    main()
