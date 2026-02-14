from pathlib import Path
from typing import Any, Dict, List, Optional
from rich.console import Console, Group
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.live import Live
from rich import box
import re
import time


COLORS = {
    "primary": "#EAB07C",  # Golden yellow
    "secondary": "#00D9FF",  # Cyan
    "success": "#00FF88",  # Green
    "error": "#FF4444",  # Red
    "warning": "#FFB800",  # Orange
    "info": "#00D9FF",  # Cyan
    "muted": "#666666",  # Gray
    "text": "#FFFFFF",  # White
}

AGENT_THEME = Theme(
    {
        "info": COLORS["info"],
        "warning": COLORS["warning"],
        "error": COLORS["error"],
        "success": COLORS["success"],
        "muted": COLORS["muted"],
        "user": COLORS["secondary"] + " bold",
        "assistant": COLORS["primary"],
        "tool": COLORS["secondary"] + " bold",
        "highlight": COLORS["primary"] + " bold",
    }
)

_console: Console | None = None


def get_console() -> Console:
    global _console
    if _console is None:
        _console = Console(theme=AGENT_THEME, highlight=False)

    return _console


class TUI:
    def __init__(self, console: Console | None = None) -> None:
        self.console = console or get_console()

    def print_banner(self):
        banner = r"""
[bold #FFB800]
    ║                                                                                                 
    ║   ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   
    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░ 
                                                                                                                
    ║                                     [#00D9FF]porti code[/#00D9FF]                                     
    ║                                                                                                  
    ║                               [dim]Your specialized AI assistant for deep coding tasks[/dim]                                  
    [/bold #FFB800]
"""
        self.console.print(banner)

    def print_welcome(self, title: str, lines: list[str]) -> None:
        self.print_banner()
        info_text = f"[bold #00D9FF]{title}[/bold #00D9FF]\n\n"
        for line in lines:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                info_text += f"[#FFB800]{parts[0]}:[/#FFB800] {parts[1]}\n"
            else:
                info_text += f"{line}\n"

        self.console.print(
            Panel(
                info_text.strip(),
                border_style="#00D9FF",
                box=box.DOUBLE,
                padding=(1, 2),
            )
        )
        self.console.print(f"[dim #666666]{'─' * 60}[/dim #666666]")

    def stream_assistant_delta(self, content: str) -> None:
        self.console.print(content, end="", markup=False)
