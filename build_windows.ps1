# Build a Windows executable from install_icons.py
# Run this on a Windows machine with Python installed.

python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt pyinstaller
pyinstaller --onefile --noconsole install_icons.py --distpath dist --workpath build --specpath build

Write-Host "Build complete. The executable is in the dist\ directory."