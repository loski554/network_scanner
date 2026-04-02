# Network Scanner

## 📌 Description
Outil de scan réseau développé en Python permettant de détecter les machines actives, d’identifier les ports ouverts et d’analyser les services associés.

## Fonctionnalités
- Détection automatique du réseau local (IP + masque)
- Scan des machines actives (ping)
- Scan des ports TCP principaux
- Résolution du hostname
- Banner grabbing (identification des services et versions)
- Multithreading pour accélérer le scan
- Export des résultats en JSON
- Système de logs

## Installation
1. Cloner le projet dans vos documents
```bash
git clone https://github.com/ton-username/network_scanner.git
cd network_scanner
```
2. Installer les dépendances
```bash
pip install -r  requirements.txt
```

## ➡️ Utilisation
```bash
# Scan automatique :
python scanner.py

# Scan manuel :
python scanner.py -n 192.168.1.0/24

# Export JSON :
python scanner.py -o resultats.json
```

## 🛠️ Technologies
- Python
- Socket
- Threading
- Manipulation réseau (IP, CIDR)

## Objectif
Comprendre le fonctionnement d'un réseau (TCP/IP)
Manipuler les sockets en python
Mettre en place un outil structuré et automatisé

## Limites/Améliorations possibles
- Certaines machines ne répondent pas au ping
- Certaines bannières peuvent être absentes

- Détection du système d’exploitation
- Interface graphique
- Barre de progression

## ✍️ Auteur
Projet réalisé par **Lucas Goulain/loski554**