import socket
import logging
import netifaces
import ipaddress
import platform
import subprocess
from ports import services

def ping_ip(ip):
    os_name = platform.system()

    if os_name == "Windows":
        command = ["ping", "-n", "1", "-w", "200", ip]
    else:
        command = ["ping", "-c", "1", "-w", "2", ip]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0

    except Exception as e:
        logging.error(f"Erreur ping {ip} -> {e}")
        return False

def scan_ports(ip):
    # Liste des ports ouverts.
    open_ports = []

    # Test pour voir si un port est ouvert avec le module socket
    # socket.socket agit comme une prise virtuelle
    # AF_INET pour une IPv4
    # SOCK_STREAM pour le protocol TCP (HTTP, SSH, HTTPS)
    # timeout pour attendre max 3ms
    # connect_ex() tentative de connexion
    # 0 > port ouvert, autre > fermé ou inaccessible

    for port, service in services.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((ip, port))

            if result == 0:
                banner = grab_banner(ip, port)
                open_ports.append({
                    "port": port,
                    "service": service,
                    "banner": banner
                })

            sock.close()

        except socket.timeout:
            logging.warning(f"Timeout sur {ip}:{port}")

        except socket.error as e:
            logging.error(f"Erreur socket {ip}:{port} -> {e}")
    
    return open_ports

# TODO
# ecrire le resumé fonction
def get_network():
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)

        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get("addr")
                netmask = addr.get("netmask")
            
                #ignore localhost
                if ip and not ip.startswith("127."):
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    return network
                
    return None

def get_hostname(ip):
    hostname = socket.getfqdn(ip)

    if hostname == ip:
        return None

    return hostname

def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))

        if port in [80, 8080]:
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            sock.send(request.encode())
        
        response = sock.recv(1024).decode(errors="ignore")
        sock.close()

        lines = response.split("\r\n")

        status = lines[0] if lines else ""
        server = None

        for line in lines:
            if line.lower().startswith("server:"):
                server = line.split(":", 1)[1].strip()

        if server:
            return f"{status} ({server})"
        else:
            return status
        
    except:
        return None