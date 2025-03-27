# network-drive-scanner
Network Drive Scanner est un outil CLI permettant de scanner et de monter automatiquement des disques réseau SMB sous Linux et macOS.
=======
# Network Drive Scanner

## Description
**Network Drive Scanner** est un outil CLI permettant de scanner et monter des disques réseau disponibles sur un réseau local. Il prend en charge les partages SMB sur les systèmes Linux et macOS. Cet outil est conçu pour automatiser la détection et le montage de disques réseau.

## Auteur
- **Mvondo Bekey Anael Sixako**
- CEO de Akamasoft
- Site web : [www.akamasoft.com](https://www.akamasoft.com)

## Fonctionnalités
- **Scan automatique** des disques réseau disponibles
- **Montage automatique** des disques détectés
- **Interface interactive** pour choisir un disque à monter
- **Exécution en arrière-plan** avec surveillance des nouveaux disques réseau

## Prérequis
- Python 3.7+
- Systèmes compatibles : Linux, macOS
- Dépendances : `inquirer`, `schedule`, `psutil`

## Installation
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/mvondo/network-drive-scanner.git
   cd network-drive-scanner
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
### Scanner les disques réseau
```bash
python network_drive_scanner.py --scan
```

### Monter un disque spécifique
```bash
python network_drive_scanner.py --mount NOM_DU_DISQUE
```

### Mode interactif
Lancer le script sans argument pour entrer dans le mode interactif :
```bash
python network_drive_scanner.py
```

## Arrêter le service en arrière-plan
Le script tourne en arrière-plan et effectue des scans réguliers.
Pour l'arrêter proprement :
```bash
pkill -f network_drive_scanner.py
```

## Contribution
Les contributions sont les bienvenues ! Vous pouvez ouvrir une issue ou proposer un pull request.

## Licence
MIT License

>>>>>>> 95c4ec4 (Initial commit)
