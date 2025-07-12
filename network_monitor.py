import psutil
from datetime import datetime
from db import get_conn
from ai_explainer import explain_network_event
from rich.console import Console

console = Console()

WHITELIST_PORTS = [22, 80, 443]

def log_network_event(event_type, details):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        '''INSERT INTO network_findings (timestamp, event_type, details)
           VALUES (?, ?, ?)''',
        (datetime.now().isoformat(), event_type, details)
    )
    conn.commit()
    conn.close()

def run_network_monitor_and_llm():
    console.print("\n [+] Checking open ports and network connections...",style="bold bright_green")
    flagged = 0

    # Check for suspicious listening ports
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN' and conn.laddr.port not in WHITELIST_PORTS:
            details = f"Listening on {conn.laddr.ip}:{conn.laddr.port} (PID {conn.pid})"
            log_network_event("suspicious_listen", details)
            console.print(f"\n  [bold red]Suspicious open port:[/bold red] {details}")
            console.print("\n  Running LLM analysis...",style="bold bright_cyan")
            try:
                insight = explain_network_event("suspicious_listen", details)
                console.print("\n  🔎 LLM Insight:",style="bold bright_yellow")
                console.print(insight,style="white")
            except Exception as e:
                console.print(f"  LLM Error: {e}",style="bold bright_red")
                console.print("\n  Have you configured your GEMINI API KEY?", style="bold bright_yellow")
                break
            flagged += 1
            console.print("\n " + "="*60, style="bold bright_black")

    # Check for established outbound connections
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.status == 'ESTABLISHED':
            details = f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port} (PID {conn.pid})"
            log_network_event("outbound_connection", details)
            print(f"\nOutbound connection: {details}")
            try:
                insight = explain_network_event("outbound_connection", details)
                console.print("\n  🔎 LLM Insight:",style="bold bright_yellow")
                console.print(insight,style="white")
            except Exception as e:
                console.print(f"  LLM Error: {e}",style="bold bright_red")
                console.print("\n  Have you configured your GEMINI API KEY?", style="bold bright_yellow")
                break
            flagged += 1
            console.print("\n " + "="*60, style="bold bright_black")

    if flagged == 0:
        console.print("  No suspicious network activity found.\n",style="bold bright_green")
