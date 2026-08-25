# Async Network & Port Scanner (CLI)

A lightweight, high-performance asynchronous IP and port scanner built with Python `asyncio` and `socket`.

## Features
- **Asynchronous Execution:** Fast subnet scanning using Python's `asyncio`.
- **CLI Support:** Flexible arguments powered by `argparse`.
- **JSON Export:** Easily export scan results for network documentation and security auditing.

## Usage

1. **Basic Scan:**
   ```bash
   python scanner.py -n 8.8.8.8/32 -p 443