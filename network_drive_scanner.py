import os
import sys
import subprocess
import threading
import platform
import schedule
import psutil
import time
import logging
import inquirer
from typing import List, Dict

def check_dependencies():
    required_packages = ['inquirer', 'schedule', 'psutil']
    missing_packages = [pkg for pkg in required_packages if not package_installed(pkg)]
    if missing_packages:
        print(f"Installation des dépendances requises : {', '.join(missing_packages)}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', *missing_packages])

def package_installed(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False

class NetworkDiskScanner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.stop_event = threading.Event()
        self.discovered_drives = []
        self.check_thread = threading.Thread(target=self._background_scan)
        self.check_thread.start()

    def _background_scan(self):
        schedule.every(10).minutes.do(self.scan_network_drives)
        while not self.stop_event.is_set():
            schedule.run_pending()
            time.sleep(60)

    def scan_network_drives(self) -> List[Dict]:
        try:
            result = subprocess.run(["smbutil", "view", "-g", "//"], capture_output=True, text=True)
            if result.returncode == 0:
                self.discovered_drives = self._parse_smb_shares(result.stdout)
                return self.discovered_drives
            else:
                self.logger.error("Erreur lors de la recherche de disques réseau")
        except Exception as e:
            self.logger.error(f"Erreur de scan: {e}")
        return []

    def _parse_smb_shares(self, scan_output: str) -> List[Dict]:
        smb_shares = []
        lines = scan_output.strip().split('\n')
        for line in lines:
            try:
                if 'smb' in line.lower():
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    smb_shares.append({
                        'protocol': 'smb',
                        'server': parts[0],
                        'share': parts[1],
                        'mount_point': f'/Volumes/smb_share_{len(smb_shares)}'
                    })
            except Exception as e:
                self.logger.error(f"Erreur lors du parsing SMB : {e}")
        return smb_shares

    def mount_drive(self, drive: Dict) -> bool:
        os_type = platform.system().lower()
        if os_type == "darwin":
            mount_cmd = ["mount_smbfs", f"//{drive['server']}{drive['share']}", drive['mount_point']]
        elif os_type == "linux":
            mount_cmd = ["mount", "-t", "cifs", f"//{drive['server']}{drive['share']}", drive['mount_point'], "-o", "guest"]
        else:
            self.logger.error("OS non supporté pour le montage réseau.")
            return False
        result = subprocess.run(mount_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            self.logger.info(f"Disque {drive['share']} monté avec succès")
            return True
        else:
            self.logger.error(f"Échec du montage de {drive['share']}: {result.stderr}")
            return False

    def interactive_mount(self):
        if not self.discovered_drives:
            self.scan_network_drives()
        if not self.discovered_drives:
            print("Aucun disque réseau détecté.")
            return
        choices = [f"{d['share']} ({d['server']})" for d in self.discovered_drives]
        question = [inquirer.List("drive", message="Sélectionnez un disque à monter", choices=choices)]
        answer = inquirer.prompt(question)
        if answer:
            selected_drive = next(d for d in self.discovered_drives if f"{d['share']} ({d['server']})" == answer['drive'])
            self.mount_drive(selected_drive)

    def stop(self):
        self.stop_event.set()
        if self.check_thread.is_alive():
            self.check_thread.join(timeout=5)

def main():
    check_dependencies()
    import argparse
    parser = argparse.ArgumentParser(description="Outil de scan et montage des disques réseau")
    parser.add_argument("--scan", action="store_true", help="Scanne les disques réseau disponibles")
    parser.add_argument("--mount", metavar="NOM", help="Monte un disque réseau par son nom")
    args = parser.parse_args()
    scanner = NetworkDiskScanner()
    if args.scan:
        drives = scanner.scan_network_drives()
        print("Disques réseau trouvés :", drives)
        return
    if args.mount:
        scanner.scan_network_drives()
        drive = next((d for d in scanner.discovered_drives if d['share'] == args.mount), None)
        if drive:
            success = scanner.mount_drive(drive)
            print("Montage réussi !" if success else "Échec du montage.")
        else:
            print("Disque non trouvé.")
        return
    scanner.interactive_mount()

if __name__ == "__main__":
    main()
