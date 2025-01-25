
import socket
import threading


def scanport(ip, port, lockthread):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            with lockthread:
                with open("portscanner.txt", "a") as file:
                    # Only write port to file if port is open
                    file.write(f"Port {port}: open\n")


if __name__ == "__main__":
    hostname = "scanme.nmap.org"
    ip = socket.gethostbyname(hostname)
    print(f"The IP address of {hostname} is {ip}")

    with open("portscanner.txt", "w") as file:
        file.write(f"Scanning IP: {ip}\n\n")

    lockthread = threading.Lock()
    threads = []

    for port in range(1, 65535 + 1):
        thread = threading.Thread(target=scanport, args=(ip, port, lockthread))
        threads.append(thread)
        thread.start()

        if len(threads) >= 1000:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()
