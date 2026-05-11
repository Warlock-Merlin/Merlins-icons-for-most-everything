# Icon Installer - Update System

This directory contains scripts for managing .ico file distribution and updates.

## Files

- **`generate_manifest.py`** - Generates a `manifest.json` file that tracks all .ico files and their MD5 hashes. Run this whenever you add new .ico files to the `Icons/` folder.
- **`install_icons.py`** - The icon installer that downloads and manages icons.
- **`create_shortcut.py`** - Creates desktop shortcuts with matching icons.
- **`main.py`** - Unified launcher that combines both functions into a simple menu.

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

4. **Users run the tool** - The unified launcher (`main.exe`) provides a menu:
   - Option 1: Install/Update Icons
   - Option 2: Create a Shortcut
   - Option 3: Exit

## How It Works

- **First Run**: Downloads and installs all .ico files
- **Subsequent Runs**: Only updates new or modified files (much faster!)
- **Version Tracking**: Both remote and local manifests have version numbers for future expansion

## Packaging as .exe

Build the unified launcher:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```

The `.exe` will be in the `dist/` folder as `main.exe`.

### Windows build support

For a Windows build, use the provided PowerShell script:
```powershell
./build_windows.ps1
```

If you want automated builds, the workflow file in `.github/workflows/build-windows.yml` runs on `windows-latest`, compiles `main.exe`, and uploads it as a workflow artifact.

## User workflow

1. User downloads `main.exe`
2. User runs `main.exe`
3. Menu appears with options to install icons or create shortcuts
4. User selects what they want to do
5. Tool handles the rest
