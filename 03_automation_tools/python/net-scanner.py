# ∞ ☬ DevRehannaLP ☬ | DevSecOps ∞ 20261603 1739
import socket


def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def scan_host(host, ports):
    print(f"\n=== Network Scanner ===")
    print(f"Scanning host: {host}")
    print(f"Ports: {ports[0]} - {ports[-1]}\n")
    open_ports = []
    for port in ports:
        if scan_port(host, port):
            print(f" [OPEN] Port {port}")
            open_ports.append(port)
    print(f"\nScan complete. {len(open_ports)} open port(s) found.")


if __name__ == "__main__":
    host = input("Enter host to scan (e.g. 127.0.0.1) ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    ports = range(start_port, end_port + 1)
    scan_host(host, ports)
