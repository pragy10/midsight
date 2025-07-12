import psutil
import time

def get_running_processes():
    """
    Returns a list of dictionaries with info about running processes.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'username', 'ppid']):
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

def detect_suspicious_processes(processes):
    """
    Returns a list of suspicious processes based on simple rules.
    """
    suspicious = []
    for p in processes:
        
        if p['exe'] and (p['exe'].startswith('/tmp') or p['exe'].startswith('/dev/shm')):
            suspicious.append((p, 'Running from tmp/shm'))

        if 'python' in p['name'].lower() and 'ssh' in p['cmdline']:
            suspicious.append((p, 'Python spawning ssh'))
            
        if not p['exe']:
            suspicious.append((p, 'No executable path'))
    return suspicious

if __name__ == "__main__":
    print("Scanning running processes...")
    procs = get_running_processes()
    sus = detect_suspicious_processes(procs)
    if sus:
        print("Suspicious processes detected:")
        for proc, reason in sus:
            print(f"PID {proc['pid']} ({proc['name']}): {reason}")
    else:
        print("No suspicious processes found.")
