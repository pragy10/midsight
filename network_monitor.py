import psutil
from datetime import datetime
from db import get_conn
from ai_explainer import explain_network_event

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
    print("\n[+] Checking open ports and network connections...")
    flagged = 0

    # Check for suspicious listening ports
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN' and conn.laddr.port not in WHITELIST_PORTS:
            details = f"Listening on {conn.laddr.ip}:{conn.laddr.port} (PID {conn.pid})"
            log_network_event("suspicious_listen", details)
            print(f"\nSuspicious open port: {details}")
            try:
                insight = explain_network_event("suspicious_listen", details)
                print("\n🔎 LLM Insight:")
                print(insight)
            except Exception as e:
                print(f"LLM Error: {e}")
            flagged += 1

    # Check for established outbound connections
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr and conn.status == 'ESTABLISHED':
            details = f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port} (PID {conn.pid})"
            log_network_event("outbound_connection", details)
            print(f"\nOutbound connection: {details}")
            try:
                insight = explain_network_event("outbound_connection", details)
                print("\n🔎 LLM Insight:")
                print(insight)
            except Exception as e:
                print(f"LLM Error: {e}")
            flagged += 1

    if flagged == 0:
        print("No suspicious network activity found.")
