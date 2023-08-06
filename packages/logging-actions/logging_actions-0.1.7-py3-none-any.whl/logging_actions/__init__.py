import argparse
import logging
from typing import Any, Callable, Iterable, Optional, Sequence, Tuple, Union

__all__ = ["log_level_action"]


def log_level_action(logger: logging.Logger):
    """Return an Action which will set the level of `logger` according to the given argument.

    Note that this does NOT add a handler. You must do that separately"""

    class LogLevelAction(argparse.Action):
        def __init__(
            self,
            option_strings: Sequence[str],
            dest: str,
            nargs: Optional[Union[int, str]] = None,
            const: Optional[str] = None,
            default: Union[str, str, None] = None,
            type: Optional[
                Union[Callable[[str], str], Callable[[str], str], argparse.FileType]
            ] = None,
            choices: Optional[Iterable[str]] = None,
            required: bool = False,
            help: Optional[str] = f"Set the logging level for {logger.name}.",
            metavar: Optional[Union[str, Tuple[str, ...]]] = None,
        ) -> None:
            try:
                # The user may have added a level, so directly consult `logging`'s internal mapping
                choices = [name.lower() for name in logging._nameToLevel.keys()]
            except Exception:
                # But that's a private API, so handle failure by falling back to the standard (documented) levels
                choices = ["critical", "error", "warning", "info", "debug", "notset"]
            if default is not None:
                logger.setLevel(default.upper())
                if help is None:
                    help = f"(default: {default})"
                else:
                    help = f"{help} (default: {default})"
            super().__init__(
                option_strings,
                dest,
                nargs=nargs,
                const=const,
                default=default,
                type=type,
                choices=choices,
                required=required,
                help=help,
                metavar=metavar,
            )

        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[str, Sequence[Any], None] = None,
            option_string: Optional[str] = None,
        ) -> None:
            if not isinstance(values, str):
                raise TypeError
            logger.setLevel(level=values.upper())
            setattr(namespace, self.dest, values)

    return LogLevelAction
