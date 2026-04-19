import os
import random
import socket
import time
import platform
import urllib.request
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
packets_sent = 0

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def run_fake_stream(duration_seconds=30):
    global packets_sent
    started_at = time.time()
    code_chars = "01ABCDEFabcdef{}[]()<>/*+-=_$#@!?:;\\|"
    event_words = ["SYN", "TLS_INIT", "ROUTE_SWAP", "PROXY_HOP", "BURST_TX", "KEEPALIVE", "RETRY", "SYNC"]
    fake_targets = ["104.22.1.15", "172.67.70.33", "185.199.111.153", "45.12.44.10", "203.0.113.77"]

    while (time.time() - started_at) < duration_seconds:
        burst = random.randint(50, 250)
        fake_target = random.choice(fake_targets)
        code_tail = "".join(random.choice(code_chars) for _ in range(random.randint(24, 52)))
        action = random.choice(event_words)
        elapsed = time.time() - started_at
        src_ip = ".".join(str(random.randint(10, 250)) for _ in range(4))
        dst_port = random.randint(1000, 65535)
        session = "".join(random.choice("0123456789abcdef") for _ in range(12))
        latency = random.randint(12, 180)
        packets_sent += burst
        total = packets_sent
        line = (
            f"[{elapsed:05.1f}s] EVT={action:<10} SID={session} SRC={src_ip}:{dst_port} "
            f"DST={fake_target}:443 COUNT={burst:03d} TOTAL={total:05d} RTT={latency}ms "
            f"PAYLOAD_SIG={code_tail}"
        )
        term_width = max(40, console.size.width - 1)
        if len(line) > term_width:
            line = line[: term_width - 3] + "..."
        console.print(line, markup=False, highlight=False, style="white")
        time.sleep(0.08)

def draw_menu():
    clear()
    banner = pyfiglet.figlet_format("SKYWALKER DDOS", font="ansi_shadow")
    console.print(banner, style="cyan")

    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_column(justify="left")

    table.add_row("[bold]1)[/bold] SKYSTART")
    table.add_row("[bold]2)[/bold] SKYIP")
    table.add_row("[bold]0)[/bold] EXIT")

    console.print(Panel(table, title="MENU", border_style="blue"))

def start_fake_flood():
    global packets_sent
    clear()
    packets_sent = 0
    console.print("SKYSTART: 12-second simulation started.\n", markup=False)
    run_fake_stream(duration_seconds=12)
    console.print("\nDONE: simulation finished. Returning to menu...", markup=False)
    time.sleep(1.0)
    clear()

def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception:
        return "Unavailable"

def get_public_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=3) as response:
            return response.read().decode().strip()
    except Exception:
        return "Unavailable"

def show_sky_ip():
    clear()
    hostname = platform.node() or socket.gethostname()
    os_name = f"{platform.system()} {platform.release()}"
    machine = platform.machine() or "Unknown"
    local_ip = get_local_ip()
    public_ip = get_public_ip()

    info_table = Table(show_header=False, box=None, pad_edge=False)
    info_table.add_column(justify="left", style="cyan")
    info_table.add_column(justify="left", style="white")
    info_table.add_row("Device", hostname)
    info_table.add_row("OS", os_name)
    info_table.add_row("Arch", machine)
    info_table.add_row("Local IP", local_ip)
    info_table.add_row("Public IP", public_ip)

    console.print(Panel(info_table, title="SKYIP", border_style="magenta"))
    console.input("Press Enter...")

def main():
    while True:
        draw_menu()
        choice = console.input("[bold blue]>> [/bold blue]").strip()
        clear()

        if choice == "1":
            start_fake_flood()

        elif choice == "2":
            show_sky_ip()

        elif choice == "0":
            os._exit(0)

        else:
            console.print("[red]Unknown option[/red]")
            console.input("Press Enter...")

if __name__ == "__main__":
    main()