import sys
from rich.console import Console
from rich.text import Text

from configure import configure_gemini_key
from db import init_db
from file_integrity import run_file_integrity_and_llm
from geoip_enricher import run_geoip_threat_enricher
from honeytoken import run_honeytoken_monitor_and_llm
from network_monitor import run_network_monitor_and_llm
from process_monitor import run_process_monitor_and_llm
from report import run_report_generator

console = Console()

def print_banner():
    try:
        import pyfiglet
        ascii_banner = pyfiglet.figlet_format("  MIDSight", font="slant")
    except Exception:
        ascii_banner = "MIDSight"
    console.print(f"[bold bright_magenta]{ascii_banner}[/bold bright_magenta]")
    console.print("[bold bright_cyan]  A Modern, Modular Linux Security CLI Tool Powered by AI[/bold bright_cyan]")
    console.print("[italic cyan]  by Pragya Sekar[/italic cyan]\n")

def main_menu():
    console.print("[bold green]  === Midsight Security CLI ===[/bold green]")
    console.print("[bold]  [1][/bold] Monitor Processes")
    console.print("[bold]  [2][/bold] File Integrity Checker")
    console.print("[bold]  [3][/bold] Network Monitor")
    console.print("[bold]  [4][/bold] GeoIP & Threat Intel Enricher")
    console.print("[bold]  [5][/bold] Honeytokens / Canary Files")
    console.print("[bold]  [6][/bold] Generate Security Report")
    console.print("[bold]  [7][/bold] Configuration")
    console.print("[bold]  [8][/bold] Exit")
    choice = console.input("[bold bright_yellow]  Type the number you wish to execute: [/bold bright_yellow]")
    return choice

if __name__ == "__main__":
    init_db()
    print_banner()
    while True:
        choice = main_menu()
        try:
            if choice == "1":
                run_process_monitor_and_llm()
            elif choice == "2":
                run_file_integrity_and_llm()
            elif choice == "3":
                run_network_monitor_and_llm()
            elif choice == "4":
                run_geoip_threat_enricher()
            elif choice == "5":
                run_honeytoken_monitor_and_llm()
            elif choice == "6":
                run_report_generator()
            elif choice== "7":
                configure_gemini_key()
            elif choice == "8":
                console.print("[bold magenta]  Exiting MIDSight. Stay safe![/bold magenta]")
                sys.exit(0)
            else:
                console.print("[bold red]  Invalid choice. Please try again.[/bold red]")
        except KeyboardInterrupt:
            console.print("\n[bold red]  [!] Operation interrupted. Returning to main menu...[/bold red]")
