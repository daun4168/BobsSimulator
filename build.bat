call venv/scripts/activate
pyinstaller -w BobsSimulator/Main.py  --clean -y --workpath work --distpath ./ --name output --icon=res/app.ico --add-data res;res
:: rd /s /q work
del output.spec
start output/output.exe

