cd ..
call venv/scripts/activate
pyinstaller -w Test/pyqt5_test.py  --clean -y --workpath work --distpath ./ --name output --icon=res/app.ico --add-data res;res
rd /s /q work
del output.spec
start output

