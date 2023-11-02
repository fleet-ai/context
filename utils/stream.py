from rich.box import MINIMAL
from rich.live import Live
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown


class TextStream:
    def __init__(self):
        self.live = Live(console=Console(), auto_refresh=False)
        self.live.start()

    def print_stream(self, message):
        markdown = Markdown(message.strip() + "●")
        panel = Panel(markdown, box=MINIMAL)
        self.live.update(panel)
        self.live.refresh()

    def end_stream(self):
        self.live.stop()
