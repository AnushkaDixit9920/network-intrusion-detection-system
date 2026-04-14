from scapy.all import sniff
from collections import defaultdict
import time
import sys

MY_IP = "172.16.77.82"

ip_activity = defaultdict(list)

THRESHOLD = 5
TIME_WINDOW = 10

LOG_FILE = "alerts.log"


def log_alert(message):
    # overwrite file → always clean
    with open(LOG_FILE, "w") as f:
        f.write(message + "\n")


def process_packet(packet):
    if packet.haslayer("IP") and packet.haslayer("TCP"):

        ip_src = packet["IP"].src

        # only track your IP
        if ip_src != MY_IP:
            return

        port = packet["TCP"].sport
        current_time = time.time()

        ip_activity[ip_src].append((port, current_time))

        ip_activity[ip_src] = [
            (p, t) for (p, t) in ip_activity[ip_src]
            if current_time - t <= TIME_WINDOW
        ]

        unique_ports = set(p for p, t in ip_activity[ip_src])

        print(f"{ip_src} → Ports: {len(unique_ports)}")

        # 🚨 Detect ONCE and EXIT immediately
        if len(unique_ports) >= THRESHOLD:
            alert_msg = f"[ALERT] Port Scan Detected from {ip_src}"
            print(alert_msg)
            print("=" * 60)

            log_alert(alert_msg)

            # 🔥 FORCE STOP (no buffering issues)
            sys.exit(0)


if __name__ == "__main__":
    print("Starting NIDS...")

    sniff(
        prn=process_packet,
        store=False
    )