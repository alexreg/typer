import shlex
from typing import Any, Optional, Sequence

import click


class ShellQuotedList(click.ParamType):
    """Converts a shell-quoted string into a list of strings."""

    name = "shell-quoted list"

    def convert(
        self,
        value: Any,
        param: Optional["click.Parameter"],
        ctx: Optional["click.Context"],
    ) -> Any:
        if value is None:
            return None
        elif isinstance(value, list):
            return value

        return shlex.split(value)

    def split_envvar_value(self, rv: str) -> Sequence[str]:
        return rv  # pragma: no cover

    def __repr__(self) -> str:
        return "SHELL-QUOTED LIST"


SHELL_QUOTED_LIST = ShellQuotedList()
