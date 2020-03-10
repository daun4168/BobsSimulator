call ../venv/scripts/activate
pyinstaller -F test.py  --clean -y
start dist/test.exe /k

