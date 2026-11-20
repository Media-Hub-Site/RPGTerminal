from __future__ import annotations

import builtins
from typing import Any
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
from rich.text import Text

# Global console to be used across the app
console = Console()
_ORIG_PRINT = builtins.print


def rprint(*objects: Any, sep: str = " ", end: str = "\n", file=None, **kwargs) -> None:
    """Rich-based replacement for builtin print.

    - Converts strings with ANSI escape codes (\033[) into Rich Ansi renderer so
      colored output from the original code is preserved.
    - Accepts the majority of usual print keyword args (sep, end)
    - kwargs are forwarded to Console.print.
    """

    text = sep.join(str(o) for o in objects)

    # If an ANSI code is present, convert it to a Rich Text object
    # (Text.from_ansi handles common ANSI sequences reliably across versions)
    if "\033[" in text:
        renderable = Text.from_ansi(text)
        console.print(renderable, end=end, **kwargs)
    else:
        console.print(text, end=end, **kwargs)


def install_rich_print() -> None:
    """Monkey-patch builtins.print to behave like rprint.

    This makes Rich print style available across the entire application without
    having to update every single call site. Call early (e.g., in `src/main.py`).
    """

    builtins.print = rprint
    

def uninstall_rich_print() -> None:
    """Restore the original builtin print.

    Useful for tests or environments that expect the normal `print`.
    """
    builtins.print = _ORIG_PRINT
