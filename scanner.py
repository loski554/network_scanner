import argparse
import ipaddress
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from utils import scan_ports, ping_ip, get_network, get_hostname
from datetime import datetime

results = []

# Fonction pour enregistrer les arguments passés
def parse_args():
    parser = argparse.ArgumentParser(description="Network Scanner")

    parser.add_argument("-n", "--network", help="Réseau cible (ex: 192.168.1.0/24)")
    parser.add_argument("-o", "--output", help="Fichier JSON de sortie")

    return parser.parse_args()

# Fonction qui vérifie si un réseau est renseigner
# sinon on lance la recherche de réseau
def get_target_network(network_arg):
    if network_arg:
        return ipaddress.ip_network(network_arg, strict=False)
    else:
        return get_network()

# Fonction qui écrit "result" dans le fichier de logs
def save_json(filename):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\nRésultats sauvegardés dans {filename}")


def scan_ip(ip):
    ip = str(ip)

    if ping_ip(ip):
        # récupération des ports ouvert pour cette ip
        ports = scan_ports(ip)

        # stockage de l'information pour le potentiel fichier json
        entry = {
            "ip": ip,
            "ports": ports
        }
        results.append(entry)

        hostname = get_hostname(ip)

        if hostname:
            print(f"[+] {ip} : {hostname}")
        else:
            print(f"[+] {ip}")
        
        for p in ports:
            if p["banner"]:
                print(f"    - {p['port']} ({p['service']}) → {p['banner']}")
            else:
                print(f"    - {p['port']} ({p['service']})")
        print()

        # ajout du log dans le fichier de logs
        logging.info(f"{ip} actif - ports: {ports}")

# Script principal
def main():
    
    # date pour rendre le fichier log unique (secondes)
    dt = datetime.now().strftime("%Y-%m-%d-%S")

    args = parse_args()

    network = get_target_network(args.network)

    if not network:
        print("Aucun réseau détecté")
        return

    print("\n=== NETWORK SCANNER ===")
    print(f"Date du scan : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    print(f"Réseau : {network}\n")

    # Liste de toutes les @IP possible sur ce réseau
    ips = list(network.hosts())

    # filename modifiable en fonction de vos dossiers
    # pour ma part j'ai choisi de faire un folder /logs
    logging.basicConfig(
        filename=f"./logs/SCANNER_{dt}.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Utilisation de ThreadPoolExecutor pour gagner du temps dans le scan
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_ip, ips)

    # Si un fichier de sortie pour les logs est renseigner
    # alors on sauvegarde le fichier
    if args.output:
        save_json(args.output)

    print("\nScan terminé.")


if __name__ == "__main__":

    main()