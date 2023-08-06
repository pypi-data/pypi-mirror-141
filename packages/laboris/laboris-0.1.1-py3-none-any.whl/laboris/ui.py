from typing import Any, Dict, List
import click
from click._compat import term_len

from laboris.model import Task


def error(*args, **kwargs):
    return click.style(*args, **kwargs, fg="red", bold=True)


def info(*args, **kwargs):
    return click.style(*args, **kwargs)


def term_width(string: str) -> int:
    return max(term_len(x) for x in string.split("\n"))


def task_short(tsk: Task):
    return (
        click.style(tsk.label, fg="blue")
        + " "
        + click.style("(" + tsk.shortUuid + ")", fg="black", bold=True)
    )


class Table(list):
    def __init__(
        self,
        header: List[str] = [],
        align: List[str] = [],
        header_style: Dict[str, Any] = {},
    ):
        self.header = header
        self.align = align
        self.header_style = header_style
        super().__init__()

    @staticmethod
    def pad(string: str, width: int, align: str = "<") -> str:
        if align == "<":
            return string + (" " * (width - term_width(string)))
        elif align == ">":
            return (" " * (width - term_width(string))) + string
        else:
            return (
                (" " * ((width - term_width(string)) // 2))
                + string
                + (" " * ((width - term_width(string)) // 2))
            )

    def raw(self) -> List[List[str]]:
        if self.header:
            return [self.header, *self]
        else:
            return self

    def get_widths(self) -> List[int]:
        widths: Dict[int, int] = {}
        for row in self:
            for idx, col in enumerate(row):
                widths[idx] = max(widths.get(idx, 0), term_width(col))

        if len(self.header) != 0:
            for idx, col in enumerate(self.header):
                widths[idx] = max(widths.get(idx, 0), term_width(col))

        return list(y for _, y in sorted(widths.items()))

    def format(self, csv: bool = False) -> str:
        widths = self.get_widths()

        if csv:
            return "\n".join(",".join(cell for cell in row) for row in self.raw())
        raw = self.raw()
        for i, row in enumerate(raw):
            raw[i] = [
                Table.pad(x, widths[j], self.align[j] if len(self.align) > j else "<")
                for j, x in enumerate(row)
            ]

        if len(self.header) != 0:
            raw[0] = [click.style(cell, **self.header_style) for cell in raw[0]]

        result = ""

        for row in raw:
            if any("\n" in x for x in row):
                lcount = max([x.count("\n") for x in row])
                for i in range(lcount + 1):
                    if i != 0:
                        result += "\n"
                    for j, cell in enumerate(row):
                        lines = cell.split("\n")
                        if j != 0:
                            result += "  "
                        if len(lines) <= i:
                            result += " " * widths[j]
                        else:
                            result += lines[i]
                pass
            else:
                result += "  ".join(cell for cell in row)
            result += "\n"

        return result.strip()

    def str(self) -> str:
        return self.format()
