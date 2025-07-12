import sys
from db import init_db
from file_integrity import run_file_integrity_and_llm
from geoip_enricher import run_geoip_threat_enricher
from honeytoken import run_honeytoken_monitor_and_llm
from network_monitor import run_network_monitor_and_llm
from process_monitor import run_process_monitor_and_llm

def main_menu():
    print("\n=== Midsight Security CLI ===")
    print("[1] Monitor Processes")
    print("[2] File Integrity Checker")
    print("[3] Network Monitor")
    print("[4] GeoIP & Threat Intel Enricher")
    print("[5] Honeytokens / Canary Files")
    print("[6] Exit")
    choice = input("Type the number you wish to execute: ").strip()
    return choice

if __name__ == "__main__":
    init_db()
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
                print("Exiting Midsight.")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n[!] Operation interrupted. Returning to main menu...")
