import os
import tarfile
from datetime import datetime
import docker

# Base directory for all backups
BACKUP_BASE_DIR = "backups"
os.makedirs(BACKUP_BASE_DIR, exist_ok=True)
# Initialize Docker client
client = docker.from_env()

# Function to list all Docker volumes
def list_volumes():
    volumes = client.volumes.list()
    print("Found the following Docker volumes:")
    for vol in volumes:
        print(f"- {vol.name}")
    return volumes

# Function to back up a Docker volume
def backup_volume(volume):
    # Create a directory for the specific volume
    volume_backup_dir = os.path.join(BACKUP_BASE_DIR, volume.name)
    os.makedirs(volume_backup_dir, exist_ok=True)
    
    # Name the backup file with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(volume_backup_dir, f"{timestamp}.tar.gz")
    
    print(f"Backing up volume: {volume.name} to {backup_file}...")
    
    # Define the path to the volume's data in WSL
    wsl_path = r"\\wsl.localhost\docker-desktop\mnt\docker-desktop-disk\data\docker\volumes"
    volume_path = os.path.join(wsl_path, volume.name, "_data")
    
    # Create a tar archive of the volume's data
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(volume_path, arcname=os.path.basename(volume_path))
    
    print(f"Backup complete: {backup_file}")

# Function to back up all Docker volumes
def backup_all_volumes():
    print("Starting backup process...")
    volumes = list_volumes()
    for volume in volumes:
        backup_volume(volume)
    print("All volumes backed up successfully!")

if __name__ == "__main__":
    backup_all_volumes()
    
