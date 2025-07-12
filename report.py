from db import get_conn
from ai_explainer import explain_overall_report
from rich.console import Console
from rich.table import Table

def fetch_counts():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM process_findings")
    process_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM file_findings")
    file_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM network_findings")
    network_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM honeytoken_findings")
    honeytoken_count = c.fetchone()[0]
    conn.close()
    return process_count, file_count, network_count, honeytoken_count

def run_report_generator():
    console = Console()
    process_count, file_count, network_count, honeytoken_count = fetch_counts()

    table = Table(title="[bold bright_magenta]      🛡️ Midsight Security Report[/bold bright_magenta]")
    table.add_column("Module", style="bright_green", no_wrap=True)
    table.add_column("Findings", style="bright_white")

    table.add_row("Process Monitor", str(process_count))
    table.add_row("File Integrity", str(file_count))
    table.add_row("Network Monitor", str(network_count))
    table.add_row("Honeytokens", str(honeytoken_count))

    console.print(table)

    try:
        summary = explain_overall_report(process_count, file_count, network_count, honeytoken_count)
        console.print("\n[bold bright_yellow]  LLM Security Summary:[/bold bright_yellow]")
        console.print(summary, style="white")
    except Exception as e:
        console.print(f"[bold bright_red]  LLM Error: {e}[/bold bright_red]")
        console.print("\n  Have you configured your GEMINI API KEY?", style="bold bright_yellow")

