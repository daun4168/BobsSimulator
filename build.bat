call venv/scripts/activate
pyinstaller BobsSimulator/__init__.py -y --workpath work --distpath ./ --name output --icon=res/app.ico --add-data res;res --add-data BobsSimulator/logging.json;BobsSimulator --additional-hooks-dir=BobsSimulator/hooks
:: rd /s /q work
:: del output.spec
start output/output.exe

