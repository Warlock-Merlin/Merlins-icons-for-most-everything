# Icon Installer - Update System

This directory contains scripts for managing .ico file distribution and updates.

## Files

- **`generate_manifest.py`** - Generates a `manifest.json` file that tracks all .ico files and their MD5 hashes. Run this whenever you add new .ico files to the `Icons/` folder.
- **`install_icons.py`** - The main installer that:
  - Downloads the latest manifest from GitHub
  - Compares it with locally installed icons
  - Only downloads and installs new or updated files
  - Saves a local manifest to track what's installed

## Workflow for Updates

1. **Add new .ico files** to the `Icons/` folder (or any subfolder like `Icons/Mail/`)

2. **Run generate_manifest.py** to update the manifest:
   ```bash
   python generate_manifest.py
   ```
   This creates/updates `manifest.json` with file hashes and sizes.

3. **Commit and push** the updated `manifest.json` to GitHub:
   ```bash
   git add manifest.json
   git commit -m "Update manifest with new icons"
   git push
   ```

4. **Users run the installer** - Whether it's their first install or an update, the installer will:
   - Check the remote manifest
   - Only download/install files that are new or have changed
   - Update their local manifest

## How It Works

- **First Run**: Downloads and installs all .ico files
- **Subsequent Runs**: Only updates new or modified files (much faster!)
- **Version Tracking**: Both remote and local manifests have version numbers for future expansion

## Packaging as .exe

Once satisfied with the installer, create an executable:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole install_icons.py
```

The `.exe` will be in the `dist/` folder.
