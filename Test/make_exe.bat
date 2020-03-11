cd ..
call venv/scripts/activate
pyinstaller -w -F Test/pyqt5_test.py  --clean -y --workpath work --distpath ./ --name output.exe
rd /s /q work
del output.exe.spec
start output.exe

