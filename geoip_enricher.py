import requests
from db import get_conn
from ai_explainer import explain_geoip_event
from rich.console import Console

console = Console()

# Free GeoIP API (ipinfo.io) and AbuseIPDB for threat checks
IPINFO_URL = "https://ipinfo.io/{ip}/json"
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"
ABUSEIPDB_API_KEY = None  # Optionally set in .env and load with os.getenv

def get_recent_network_events(limit=10):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM network_findings ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def geoip_lookup(ip):
    try:
        r = requests.get(IPINFO_URL.format(ip=ip), timeout=5)
        if r.status_code == 200:
            data = r.json()
            return f"{data.get('city','')}, {data.get('region','')}, {data.get('country','')}"
    except Exception:
        pass
    return "Unknown location"

def check_blacklist(ip):
    if not ABUSEIPDB_API_KEY:
        return "AbuseIPDB API key not set"
    headers = {'Key': ABUSEIPDB_API_KEY, 'Accept': 'application/json'}
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}
    try:
        r = requests.get(ABUSEIPDB_URL, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data['data']['abuseConfidenceScore'] > 0:
                return f"Listed (Score: {data['data']['abuseConfidenceScore']})"
            else:
                return "Not listed"
    except Exception:
        pass
    return "Check failed"

def extract_ip(details):
    # Try to extract an IP address from a string like "1.2.3.4:5678 -> 8.8.8.8:80"
    import re
    match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})', details)
    return match.group(1) if match else None

def run_geoip_threat_enricher():
    console.print("\n [+] Enriching recent network events with GeoIP and threat intel...", style="bold bright_green")
    events = get_recent_network_events()
    flagged = 0
    for event in events:
        ip = extract_ip(event[3])  # details field
        if ip:
            location = geoip_lookup(ip)
            blacklist = check_blacklist(ip)
            console.print(f"\n  [bold white]Event:[/bold white] {event[2]} | [bold white]Details:[/bold white] {event[3]}")
            console.print(f"  [bold white]IP:[/bold white] {ip}")
            console.print(f"  [bold white]Location:[/bold white] {location}")
            console.print(f"  [bold white]Blacklist:[/bold white] {blacklist}")
            console.print("\n  Running LLM analysis...", style="bold bright_cyan")
            try:
                insight = explain_geoip_event(event[2], ip, location, blacklist)
                console.print("\n 🔎 [bold bright_yellow]LLM Insight:[/bold bright_yellow]")
                console.print(insight, style="white")
            except Exception as e:
                console.print(f"  LLM Error: {e}", style="bold bright_red")
                console.print("\n  Have you configured your GEMINI API KEY?", style="bold bright_yellow")
                break
            flagged += 1
            console.print(" \n " + "="*60, style="bold bright_black")
    if flagged == 0:
        console.print("  No recent network events with extractable IPs found.\n", style="bold bright_green")

