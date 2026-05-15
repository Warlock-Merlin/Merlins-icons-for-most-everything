import json
import os
import hashlib

# Path to the Icons folder
ICONS_FOLDER = "Icons"

# Output manifest file
MANIFEST_FILE = "manifest.json"

def calculate_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def set_hidden_windows(path):
    if os.name == "nt" and os.path.exists(path):
        os.system(f'attrib +h "{path}"')


def generate_manifest():
    """Generate manifest.json from the Icons folder."""
    manifest = {
        "version": "1.0",
        "files": {}
    }
    
    if not os.path.exists(ICONS_FOLDER):
        print(f"Error: '{ICONS_FOLDER}' folder not found.")
        return
    
    # Walk through the Icons folder
    for root, dirs, files in os.walk(ICONS_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            # Create a relative path for the manifest
            relative_path = os.path.relpath(file_path, ICONS_FOLDER)
            
            # Calculate hash and size
            file_hash = calculate_file_hash(file_path)
            file_size = os.path.getsize(file_path)
            
            manifest["files"][relative_path] = {
                "hash": file_hash,
                "size": file_size
            }
    
    # Save manifest to file
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    set_hidden_windows(MANIFEST_FILE)
    print(f"Manifest generated: {MANIFEST_FILE} (hidden on Windows)")
    print(f"Total files: {len(manifest['files'])}")

if __name__ == "__main__":
    generate_manifest()
