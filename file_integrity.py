import os
import hashlib
import json
from datetime import datetime
from db import get_conn
from ai_explainer import explain_file_change
from rich.console import Console

console = Console()

MONITORED_FILES = [
    '/etc/passwd',
    '/etc/shadow',
    '/etc/ssh/sshd_config',
    '/etc/crontab',
    os.path.expanduser('~/.bashrc')
]

BASELINE_FILE = os.path.expanduser('~/.midsight/file_baseline.json')

def hash_file(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def create_baseline():
    baseline = {f: hash_file(f) for f in MONITORED_FILES}
    with open(BASELINE_FILE, 'w') as f:
        json.dump(baseline, f)
    print("File integrity baseline created.")

def check_integrity_and_log():
    if not os.path.exists(BASELINE_FILE):
        console.print(" [+]No baseline found. Creating one now...", style="bold bright_yellow")
        create_baseline()
        return

    with open(BASELINE_FILE) as f:
        baseline = json.load(f)

    any_change = False
    for fpath in MONITORED_FILES:
        current_hash = hash_file(fpath)
        old_hash = baseline.get(fpath)
        if old_hash != current_hash:
            any_change = True
            console.print(f"\n  [bold red][!] Change detected in:[/bold red] {fpath}")
            log_file_change(fpath, "modified", f"Hash changed: {old_hash} -> {current_hash}")
            console.print("\n  Running LLM analysis...", style="bold bright_cyan")
            try:
                insight = explain_file_change(fpath, "modified", old_hash, current_hash)
                console.print("\n  🔎 [bold bright_yellow]LLM Insight:[/bold bright_yellow]")
                console.print(insight, style="white")
            except Exception as e:
                console.print(f"  LLM Error: {e}", style="bold bright_red")
                console.print("\n  Have you configured your GEMINI API KEY?", style="bold bright_yellow")
                break
            console.print("\n " + "="*60, style="bold bright_black")
    if not any_change:
        console.print(" No file changes detected.\n", style="bold green")


def log_file_change(file_path, change_type, details):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        '''INSERT INTO file_findings (timestamp, file_path, change_type, details)
           VALUES (?, ?, ?, ?)''',
        (datetime.now().isoformat(), file_path, change_type, details)
    )
    conn.commit()
    conn.close()

def run_file_integrity_and_llm():
    check_integrity_and_log()
