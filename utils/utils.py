import re
import traceback

from rich import print as rprint
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel


console = Console()


def print_markdown(message):
    for line in message.split("\n"):
        line = line.strip()
        if line == "":
            print("")
        elif line == "---":
            rprint(Rule(style="white"))
        elif line.startswith("!!!"):
            rprint(Text(line[3:], style="#D5D7FB"))
        else:
            rprint(Markdown(line))

    if "\n" not in message and message.startswith(">"):
        print("")


def print_exception(exc_type, exc_value, traceback_obj):
    traceback_details = traceback.extract_tb(traceback_obj)
    for filename, lineno, funcname, text in traceback_details:
        console.print(
            f"File: {filename}, Line: {lineno}, Func: {funcname}, Text: {text}"
        )
    console.print(f"{exc_type.__name__}: {exc_value}")


def extract_code_blocks(message):
    pattern = r"```python\n(.*?)```"
    matches = re.findall(pattern, message, re.DOTALL)
    return "\n".join(matches)


def print_help():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Command")
    table.add_column("Description")

    # Add rows to the table for each command
    table.add_row("-k, --k_value", "Number of chunks to return")
    table.add_row(
        "-l, --libraries",
        "Limit your chat to a list of libraries. Usage: -l library1 library2 library3",
    )
    table.add_row(
        "-m, --model", "Specify the model. Default: gpt-4-1106-preview (gpt-4-turbo)"
    )
    table.add_row(
        "-c, --cite_sources", "Determines whether or not the AI model cites its sources"
    )
    table.add_row("-h, --help", "Help")

    # Create a panel with the table
    panel = Panel(table, title="Help", border_style="blue")

    # Print the panel
    rprint(panel)
