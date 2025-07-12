import os
import time
from datetime import datetime
from db import get_conn
from ai_explainer import explain_honeytoken_event

# List of honeytoken files to monitor
HONEYTOKENS = [
    os.path.expanduser('~/.midsight/passwd.bak'),
    os.path.expanduser('~/.midsight/fake_ssh_key'),
    os.path.expanduser('~/.midsight/secret_cronjob')
]

def create_honeytokens():
    for f in HONEYTOKENS:
        if not os.path.exists(f):
            with open(f, 'w') as fp:
                fp.write("DO NOT TOUCH\n")
    print("Honeytoken files created.")

def log_honeytoken_event(file_path, event_type, details):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        '''INSERT INTO honeytoken_findings (timestamp, file_path, event_type, details)
           VALUES (?, ?, ?, ?)''',
        (datetime.now().isoformat(), file_path, event_type, details)
    )
    conn.commit()
    conn.close()

def monitor_honeytokens():
    print("\n[+] Monitoring honeytoken files for access or changes (Ctrl+C to stop)...")
    # Store initial access and modification times
    file_stats = {}
    for f in HONEYTOKENS:
        if os.path.exists(f):
            stat = os.stat(f)
            file_stats[f] = (stat.st_atime, stat.st_mtime)
    try:
        while True:
            for f in HONEYTOKENS:
                if os.path.exists(f):
                    stat = os.stat(f)
                    atime, mtime = stat.st_atime, stat.st_mtime
                    old_atime, old_mtime = file_stats.get(f, (atime, mtime))
                    if atime != old_atime:
                        log_honeytoken_event(f, "access", f"Access time changed: {old_atime} -> {atime}")
                        print(f"\n[!] Honeytoken accessed: {f}")
                        try:
                            insight = explain_honeytoken_event(f, "access")
                            print("\n🔎 LLM Insight:")
                            print(insight)
                        except Exception as e:
                            print(f"LLM Error: {e}")
                    if mtime != old_mtime:
                        log_honeytoken_event(f, "modified", f"Modification time changed: {old_mtime} -> {mtime}")
                        print(f"\n[!] Honeytoken modified: {f}")
                        try:
                            insight = explain_honeytoken_event(f, "modified")
                            print("\n🔎 LLM Insight:")
                            print(insight)
                        except Exception as e:
                            print(f"LLM Error: {e}")
                    file_stats[f] = (atime, mtime)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Honeytoken monitoring stopped. Returning to main menu...")

def run_honeytoken_monitor_and_llm():
    create_honeytokens()
    monitor_honeytokens()
