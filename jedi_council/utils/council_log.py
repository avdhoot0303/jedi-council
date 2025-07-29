from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

council_banner = r"""
       █████              █████  ███       █████████                                           ███  ████    
      ░░███              ░░███  ░░░       ███░░░░░███                                         ░░░  ░░███    
       ░███   ██████   ███████  ████     ███     ░░░   ██████  █████ ████ ████████    ██████  ████  ░███    
       ░███  ███░░███ ███░░███ ░░███    ░███          ███░░███░░███ ░███ ░░███░░███  ███░░███░░███  ░███    
       ░███ ░███████ ░███ ░███  ░███    ░███         ░███ ░███ ░███ ░███  ░███ ░███ ░███ ░░░  ░███  ░███    
 ███   ░███ ░███░░░  ░███ ░███  ░███    ░░███     ███░███ ░███ ░███ ░███  ░███ ░███ ░███  ███ ░███  ░███    
░░████████  ░░██████ ░░████████ █████    ░░█████████ ░░██████  ░░████████ ████ █████░░██████  █████ █████   
 ░░░░░░░░    ░░░░░░   ░░░░░░░░ ░░░░░      ░░░░░░░░░   ░░░░░░    ░░░░░░░░ ░░░░ ░░░░░  ░░░░░░  ░░░░░ ░░░░░    

                         JEDI COUNCIL · LLM CENTRAL
"""

def show_banner():
    console.print(council_banner, style="cyan")

def log_consultation(model_name: str, wisdom: str, usage: str, cost: float, latency: int):
    console.print(Panel.fit(f"🔮 [bold cyan]Consulting the Jedi Council[/bold cyan]"))
    console.print(f"[bold]Model:[/bold] {model_name}", style="yellow")
    console.print(f"[green]Wisdom:[/green] {wisdom}")
    console.print(f"[dim]Usage:[/dim] {usage}    [blue]Cost:[/blue] ${cost:.6f}    [magenta]Latency:[/magenta] {latency}ms\n")