import asyncio
import argparse
import json
import socket
from ipaddress import ip_network
from datetime import datetime


async def check_port(ip, port, timeout=1):
    """بررسی باز بودن یک پورت مشخص روی IP تعیین شده"""
    try:
        conn = asyncio.open_connection(str(ip), port)
        _, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return str(ip), port, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return str(ip), port, False


async def scan_network(network_cidr, port, output_file=None):
    """اسکن همزمان تمام IPهای موجود در یک Subnet و خروجی ساختاریافته"""
    net = ip_network(network_cidr, strict=False)
    tasks = []

    print(f"[*] Starting scan on {network_cidr} for port {port}...\n")

    for ip in net.hosts():
        tasks.append(check_port(ip, port))

    results = await asyncio.gather(*tasks)

    open_hosts = []
    for ip, port, is_open in results:
        if is_open:
            print(f"[+] {ip}:{port} is OPEN")
            open_hosts.append({"ip": ip, "port": port, "status": "OPEN"})

    print(f"\n[*] Scan finished. Found {len(open_hosts)} open port(s).")

    # ذخیره خروجی در فایل JSON در صورت درخواست کاربر
    if output_file and open_hosts:
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "target_network": network_cidr,
            "scanned_port": port,
            "open_hosts": open_hosts
        }
        with open(output_file, "w") as f:
            json.dump(report_data, f, indent=4)
        print(f"[+] Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Async Python Network & Port Scanner")
    parser.add_argument("-n", "--network", type=str, default="8.8.8.8/32",
                        help="Target CIDR network (e.g., 192.168.1.0/28)")
    parser.add_argument("-p", "--port", type=int, default=443,
                        help="Target TCP port (e.g., 80, 443, 22)")
    parser.add_argument("-o", "--output", type=str,
                        default=None, help="Output JSON file path")

    args = parser.parse_args()

    asyncio.run(scan_network(args.network, args.port, args.output))
