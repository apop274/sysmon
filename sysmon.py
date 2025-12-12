#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import time
from datetime import datetime

def run(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def cpu_percent() -> float:
    #snapshot
    out = run("LC_ALL=C top -bn1 | grep 'Cpu(s)'")
    #example:: "Cpu(s):  2.0%us,  1.0%sy,  0.0%ni, 96.7%id, ..."
    parts = out.replace(",", "").split()
    idle = float(parts[parts.index("id") - 1].replace("%", ""))
    return round(100.0 - idle, 1)

def mem_line() -> tuple[str, str]:
    
    used = run("free -h | awk '/Mem:/ {print $3}'")
    total = run("free -h | awk '/Mem:/ {print $2}'")
    return used, total

def disk_line(path: str) -> tuple[str, str]:
    used = run(f"df -h '{path}' | awk 'NR==2 {{print $3}}'")
    total = run(f"df -h '{path}' | awk 'NR==2 {{print $2}}'")
    return used, total

def main():
    p = argparse.ArgumentParser(
        prog="sysmon",
        description="Lightweight Linux system monitor + logger (CPU/RAM/Disk)."
    )
    p.add_argument("-i", "--interval", type=float, default=2.0, help="Seconds between updates (default: 2)")
    p.add_argument("-n", "--count", type=int, default=0, help="Number of updates then exit (0 = run forever)")
    p.add_argument("--disk-path", default="/", help="Path to check disk usage for (default: /)")
    p.add_argument("--log", default="", help="Append output to this file")
    p.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    args = p.parse_args()

    use_color = (not args.no_color) and shutil.which("tput") is not None

    def color(s: str, code: str) -> str:
        if not use_color:
            return s
        return f"\033[{code}m{s}\033[0m"

    k = 0
    try:
        while True:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu = cpu_percent()
            ram_used, ram_total = mem_line()
            d_used, d_total = disk_line(args.disk_path)

            line = (
                f"{ts} | "
                f"CPU {color(f'{cpu:>4.1f}%', '36')} | "
                f"RAM {color(f'{ram_used}/{ram_total}', '35')} | "
                f"DISK({args.disk_path}) {color(f'{d_used}/{d_total}', '33')}"
            )

            print(line)

            if args.log:
                with open(args.log, "a", encoding="utf-8") as f:
                    f.write(line + "\n")

            k += 1
            if args.count and k >= args.count:
                break

            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
