import socket
import time

target = "172.16.77.82"

print("Starting Port Scan Simulation...")

for port in range(20, 500):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)

    try:
        s.connect((target, port))
    except:
        pass

    s.close()
  

print("Attack finished.")