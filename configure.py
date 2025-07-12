import pwinput
from rich.console import Console

console = Console()

def configure_gemini_key():
    from pathlib import Path
    import sys

    env_path = Path(".env")
    console.print("\n[bold cyan]  === Configuration ===[/bold cyan]")
    key = pwinput.pwinput(prompt="  Enter your Gemini API Key: ", mask="*").strip()
    if not key:
        console.print("[bold red]  No key entered. Configuration aborted.[/bold red]")
        sys.exit(0)
    lines = []
    if env_path.exists():
        with env_path.open("r") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("GEMINI_API_KEY="):
            lines[i] = f"GEMINI_API_KEY={key}\n"
            found = True
            break
    if not found:
        lines.append(f"GEMINI_API_KEY={key}\n")
    with env_path.open("w") as f:
        f.writelines(lines)
    console.print("[bold bright_green]  Gemini API key saved to .env![/bold bright_green]")
    console.print("  Restart the service!\n", style="bright_green")
    sys.exit(0)
