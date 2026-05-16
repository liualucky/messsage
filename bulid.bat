@echo off
python -m pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed --icon=assets\app.ico main.py
pause