import requests
import zipfile
import shutil
import os
import tempfile
import json
import hashlib

# GitHub URLs
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Warlock-Merlin/Merlins-icons-for-most-everything/main/manifest.json"
GITHUB_ZIP_URL = "https://github.com/Warlock-Merlin/Merlins-icons-for-most-everything/archive/refs/heads/main.zip"

# Destination folder on C drive
DEST_FOLDER = "C:\\.ico"

# Local manifest file to track installed versions
LOCAL_MANIFEST = os.path.join(DEST_FOLDER, "manifest.json")

def calculate_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def load_local_manifest():
    """Load the local manifest if it exists."""
    if os.path.exists(LOCAL_MANIFEST):
        try:
            with open(LOCAL_MANIFEST, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load local manifest: {e}")
    return {"version": "0.0", "files": {}}

def download_remote_manifest():
    """Download the manifest from GitHub."""
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error downloading manifest: {e}")
        return None

def get_files_to_update(remote_manifest, local_manifest):
    """Determine which files need to be downloaded/updated."""
    files_to_update = []
    
    remote_files = remote_manifest.get("files", {})
    local_files = local_manifest.get("files", {})
    
    for file_path, file_info in remote_files.items():
        local_info = local_files.get(file_path)
        # Update if file doesn't exist locally or hash differs
        if local_info is None or local_info.get("hash") != file_info.get("hash"):
            files_to_update.append(file_path)
    
    return files_to_update, remote_files

def download_and_extract_icons():
    try:
        print("Checking for updates...")
        
        # Download remote manifest
        remote_manifest = download_remote_manifest()
        if remote_manifest is None:
            print("Error: Could not retrieve manifest from GitHub.")
            return
        
        # Load local manifest
        local_manifest = load_local_manifest()
        
        # Check version
        remote_version = remote_manifest.get("version")
        local_version = local_manifest.get("version")
        
        # Get files that need updating
        files_to_update, remote_files = get_files_to_update(remote_manifest, local_manifest)
        
        if not files_to_update and remote_version == local_version:
            print("All icons are up to date!")
            return
        
        print(f"Found {len(files_to_update)} file(s) to update.")
        
        # Download the zip
        print("Downloading from GitHub...")
        response = requests.get(GITHUB_ZIP_URL)
        response.raise_for_status()
        
        # Create a temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "repo.zip")
            
            # Save the zip
            with open(zip_path, "wb") as f:
                f.write(response.content)
            
            # Extract the zip
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the extracted Icons folder
            extracted_repo_dir = os.path.join(temp_dir, "Merlins-icons-for-most-everything-main")
            icons_source = os.path.join(extracted_repo_dir, "Icons")
            
            if not os.path.exists(icons_source):
                print("Error: Icons folder not found in the downloaded archive.")
                return
            
            # Ensure destination exists
            os.makedirs(DEST_FOLDER, exist_ok=True)
            
            # Copy only updated files
            print("Installing/updating icons...")
            for file_path in files_to_update:
                source_file = os.path.join(icons_source, file_path)
                dest_file = os.path.join(DEST_FOLDER, file_path)
                
                if os.path.exists(source_file):
                    # Create destination directory if needed
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    shutil.copy2(source_file, dest_file)
        
        # Update local manifest
        local_manifest = remote_manifest
        with open(LOCAL_MANIFEST, "w") as f:
            json.dump(local_manifest, f, indent=2)
        
        print(f"Successfully updated {len(files_to_update)} file(s) in '{DEST_FOLDER}'.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading from GitHub: {e}")
    except Exception as e:
        print(f"Error during installation: {e}")

if __name__ == "__main__":
    download_and_extract_icons()