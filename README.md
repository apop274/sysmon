## sysmon

A lightweight Linux CLI system monitor + logger that prints CPU usage, RAM usage, and disk usage at a configurable interval.

## Features
- Displays **CPU %, RAM used/total, Disk used/total**
- Configurable update interval
- Optional logging to a file
- Color output (can be disabled)

## Requirements
- Linux (tested on Linux Mint / Ubuntu)
- Python 3

## Usage

  1. Download (clone) the repository
    ```bash
    git clone https://github.com/apop274/sysmon.git

  2. Enter the project folder:
     cd sysmon

  3. Run it (you can sto any time with Ctrl+C):

     **Prints one line every 2 seconds until you stop it:**
     python3 sysmon.py

     **Print 10 updates then exit:**
     python3 sysmon.py --count 10

     Print once every 10 seconds:
     python3 sysmon.py --interval 10

     Log output to a file (logs 50 updates to stats.log):
     python3 sysmon.py --interval 2 --count 50 --log stats.log

     Log forever:
     python3 sysmon.py --log stats.log

     Check disk usage for a specific path a print 10 updates:
     python3 sysmon.py --disk-path /home --count 10

     Diable ANSI colors:
     python3 sysmon.py --no-color --count 10

     Combining multiple flags (typical usage):
     python3 sysmon.py --interval 2 --count 30 --log stats.log --disk-path /


