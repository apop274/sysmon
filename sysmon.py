#!/usr/bin/env python3
"""
sysmon.py

A lightweight Linux CLI system monitor + logger.
Reports CPU usage, RAM usage, and disk usage at a configurable interval.
Supports optional logging to a file.

Designed to be simple, portable, and Linux-native.
"""

import argparse
import subprocess
import time
from datetime import datetime
import shutil


def run(cmd: str) -> str:
    """
    Run a shell command and return its output as a string.
    """
    return subprocess.check_output(cmd, shell=True, text=True).strip()


def cpu_percent() -> float:
    #snapshot
    out = run("LC_ALL=C top -bn1 | grep 'Cpu(s)'")
    #example:: "Cpu(s):  2.0%us,  1.0%sy,  0.0%ni, 96.7%id, ..."
    """
    Estimate CPU usage using a single snapshot from `top`.

    We parse the idle percentage and subtract from 100.
    """
    out = run("LC_ALL=C top -bn1 | grep 'Cpu(s)'")
    parts = out.replace(",", "").split()

    # Find idle percentage and compute usage
    idle = float(parts[parts.index("id") - 1].replace("%", ""))
    return round(100.0 - idle, 1)

def mem_line() -> tuple[str, str]:
    used = run)"free -h | awk '/Mem:/ {print $3}'")
    total = run("free -h | awk '/Mem:/ {print $2}'")
    return used, total

def memory_usage() -> tuple[str, str]:
    """
    Return used and total RAM in human-readable format.
    """
    used = run("free -h | awk '/Mem:/ {print $3}'")
    total = run("free -h | awk '/Mem:/ {print $2}'")
    return used, total


def disk_usage(path: str) -> tuple[str, str]:
    """
    Return used and total disk usage for a given path.
    """
    used = run(f"df -h '{path}' | awk 'NR==2 {{print $3}}'")
    total = run(f"df -h '{path}' | awk 'NR==2 {{print $2}}'")
    return used, total


def main():
    """
    Main CLI entry point.
    Parses arguments and runs the monitoring loop.
    """
    parser = argparse.ArgumentParser(
        prog="sysmon",
        description="Lightweight Linux system monitor + logger (CPU/RAM/Disk)."
    )

    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=2.0,
        help="Seconds between updates (default: 2)"
    )

    parser.add_argument(
        "-n", "--count",
        type=int,
        default=0,
        help="Number of updates before exit (0 = run forever)"
    )

    parser.add_argument(
        "--disk-path",
        default="/",
        help="Path to check disk usage for (default: /)"
    )

    parser.add_argument(
        "--log",
        default="",
        help="Append output to this file"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors"
    )

    args = parser.parse_args()

    # Enable colors only if allowed and terminal supports it
    use_color = (not args.no_color) and shutil.which("tput") is not None

    def color(text: str, code: str) -> str:
        if not use_color:
            return text
        return f"\033[{code}m{text}\033[0m"

    iteration = 0

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cpu = cpu_percent()
            ram_used, ram_total = memory_usage()
            disk_used, disk_total = disk_usage(args.disk_path)

            line = (
                f"{timestamp} | "
                f"CPU {color(f'{cpu:>5.1f}%', '36')} | "
                f"RAM {color(f'{ram_used}/{ram_total}', '35')} | "
                f"DISK({args.disk_path}) {color(f'{disk_used}/{disk_total}', '33')}"
            )

            print(line)

            # Optional logging
            if args.log:
                with open(args.log, "a", encoding="utf-8") as f:
                    f.write(line + "\n")

            iteration += 1
            if args.count and iteration >= args.count:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        pass


if __name__ == "__main__":
    main()

