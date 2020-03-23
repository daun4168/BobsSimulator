call venv/scripts/activate
:: pyinstaller BobsSimulator/__init__.py -y --workpath work --distpath ./ --name output --icon=res/app.ico --add-data res;res --add-data BobsSimulator/logging.json;BobsSimulator --additional-hooks-dir=BobsSimulator/hooks --hidden-import=hearthstone --hidden-import=hearthstone_data
:: pyinstaller BobsSimulator/__init__.py -y --clean --workpath output/work --distpath ./ --name output --icon=res/app.ico --add-data res;res --add-data BobsSimulator/logging.json;BobsSimulator --additional-hooks-dir=BobsSimulator/hooks --hidden-import=hearthstone --hidden-import=hearthstone_data  --hidden-import=pkg_resources  --path=C:\Users\main\PycharmProjects\BobsSimulator\venv\Lib\site-packages --path=C:\Users\main\PycharmProjects\BobsSimulator\venv
:: rd /s /q work
:: del output.spec
pyinstaller -y --clean --workpath build/work --distpath build build.spec
start build/output/output.exe

