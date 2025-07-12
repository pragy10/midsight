import psutil
from datetime import datetime
from db import get_conn
from ai_explainer import explain_process
from rich.console import Console

console = Console()

KERNEL_PREFIXES = [
    "kworker", "ksoftirqd", "migration", "rcu_", "kauditd", "watchdogd", "ksmd", "khugepaged"
]
SYSTEM_USERS = ['root', 'systemd-network', 'syslog', 'messagebus', 'daemon']

def is_kernel_thread(proc_name):
    return any(proc_name.startswith(prefix) for prefix in KERNEL_PREFIXES)

def is_system_user(user):
    return user in SYSTEM_USERS

def is_suspicious(proc):
    if is_kernel_thread(proc['name']):
        return False
    if is_system_user(proc['username']) and not (proc['username'] == 'root' and proc['exe'] and proc['exe'].startswith('/home')):
        return False
    if proc['exe'] and (proc['exe'].startswith('/tmp') or proc['exe'].startswith('/dev/shm')):
        return True
    if 'python' in proc['name'].lower() and 'ssh' in proc['cmdline']:
        return True
    if proc['username'] == 'root' and proc['exe'] and proc['exe'].startswith('/home'):
        return True
    if 'base64' in proc['cmdline'] or 'nc ' in proc['cmdline'] or 'bash -i' in proc['cmdline']:
        return True
    return False

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'exe', 'cmdline', 'username']):
        try:
            info = proc.info
            processes.append({
                'pid': info['pid'],
                'ppid': info['ppid'],
                'name': info['name'],
                'exe': info.get('exe', ''),
                'cmdline': ' '.join(info.get('cmdline', [])),
                'username': info['username']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def log_suspicious_process(proc, reason):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        '''INSERT INTO process_findings (timestamp, pid, ppid, name, exe, cmdline, username, reason)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (datetime.now().isoformat(), proc['pid'], proc['ppid'], proc['name'], proc['exe'], proc['cmdline'], proc['username'], reason)
    )
    conn.commit()
    conn.close()

def run_process_monitor_and_llm():
    console.print("\n [+] Scanning running processes for suspicious activity...", style="bold bright_green")
    procs = get_running_processes()
    flagged = 0
    for proc in procs:
        if is_suspicious(proc):
            log_suspicious_process(proc, "Flagged by rule")
            console.print(f"\n[bold red]  Suspicious process detected:[/bold red] PID {proc['pid']} ({proc['name']})")
            console.print(f"  [bold white]Executable:[/bold white] {proc['exe']}")
            console.print(f"  [bold white]Cmdline:[/bold white] {proc['cmdline']}")
            console.print("\n  Running LLM analysis...", style="bold bright_cyan")
            proc_row = (
                None, datetime.now().isoformat(), proc['pid'], proc['ppid'],
                proc['name'], proc['exe'], proc['cmdline'], proc['username'], "Flagged by rule"
            )
            try:
                insight = explain_process(proc_row)
                console.print("\n  🔎 [bold bright_yellow]LLM Insight:[/bold bright_yellow]")
                console.print(insight, style="white")
            except Exception as e:
                console.print(f"  LLM Error: {e}", style="bold bright_red")
                console.print("\n  Have you configured your GEMINI API KEY?", style="bold bright_yellow")
                break
            flagged += 1
            console.print(" \n " + "="*60, style="bold bright_black")
    if flagged == 0:
        console.print(" No suspicious processes found.\n", style="bold green")


# No need for if __name__ == "__main__" block here, as this will be called from main.py
