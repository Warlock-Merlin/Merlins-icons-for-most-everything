# Build a Windows executable from main.py
# Run this on a Windows machine with Python installed.

python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt pyinstaller
pyinstaller --onefile --noconsole main.py --distpath dist --workpath build --specpath build

Write-Host "Build complete. The executable is in the dist\ directory."
