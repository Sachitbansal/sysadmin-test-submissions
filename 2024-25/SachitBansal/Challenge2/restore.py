import os
import tarfile
from datetime import datetime

# Base directory for all backups
BACKUP_BASE_DIR = "backups"
os.makedirs(BACKUP_BASE_DIR, exist_ok=True)

# Function to restore a Docker volume from a specific backup
def restore_volume(volume_name, backup_file):
    # Path to the volume's data in WSL
    wsl_path = r"\\wsl.localhost\docker-desktop\mnt\docker-desktop-disk\data\docker\volumes"
    volume_path = os.path.join(wsl_path, volume_name)
    
    print(f"Restoring volume: {volume_name} from {backup_file}...")
    
    # Extract the backup archive into the volume's data directory
    with tarfile.open(backup_file, "r:gz") as tar:
        tar.extractall(path=volume_path)
    
    print(f"Restoration complete for volume: {volume_name}")

# Function to restore backups for a specific volume
def restore_backup_for_volume():
    # List all volume directories in the backup base directory
    volume_dirs = [d for d in os.listdir(BACKUP_BASE_DIR) if os.path.isdir(os.path.join(BACKUP_BASE_DIR, d))]
    
    # Prompt user to choose a volume to restore
    print(f"Available volumes with backups: {volume_dirs}")
    volume_name = input("Enter the volume name to restore: ").strip()
    
    if volume_name not in volume_dirs:
        print(f"Volume {volume_name} does not exist in the backups.")
        return
    
    # Path to the specific volume's backup directory
    volume_backup_dir = os.path.join(BACKUP_BASE_DIR, volume_name)
    backup_files = [f for f in os.listdir(volume_backup_dir) if f.endswith(".tar.gz")]
    
    if not backup_files:
        print(f"No backups available for volume {volume_name}.")
        return
    
    # Sort backups by timestamp (latest first)
    backup_files.sort(reverse=True)
    print(f"Available backups for volume {volume_name}: {backup_files}")
    
    # Prompt user to choose a backup (default to the latest if no input is given)
    chosen_backup = input(f"Enter the backup file to restore (default is {backup_files[0]}): ").strip()
    if not chosen_backup:
        chosen_backup = backup_files[0]
    
    # Validate the chosen backup
    if chosen_backup not in backup_files:
        print(f"Backup {chosen_backup} does not exist.")
        return
    
    # Restore the chosen backup
    backup_file = os.path.join(volume_backup_dir, chosen_backup)
    restore_volume(volume_name, backup_file)

if __name__ == "__main__":
    # Uncomment the next line to back up all volumes
    # backup_all_volumes()
    
    # Uncomment the next line to restore a volume's backup
    restore_backup_for_volume()
    pass
