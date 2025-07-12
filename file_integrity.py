import os
import hashlib
import json
from datetime import datetime
from db import get_conn
from ai_explainer import explain_file_change

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
        print("No baseline found. Creating one now...")
        create_baseline()
        return

    with open(BASELINE_FILE) as f:
        baseline = json.load(f)

    for fpath in MONITORED_FILES:
        current_hash = hash_file(fpath)
        old_hash = baseline.get(fpath)
        if old_hash != current_hash:
            print(f"\n[!] Change detected in: {fpath}")
            log_file_change(fpath, "modified", f"Hash changed: {old_hash} -> {current_hash}")
            try:
                insight = explain_file_change(fpath, "modified", old_hash, current_hash)
                print("\n🔎 LLM Insight:")
                print(insight)
            except Exception as e:
                print(f"LLM Error: {e}")

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
