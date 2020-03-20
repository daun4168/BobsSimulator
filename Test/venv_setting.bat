cd ..
call venv/scripts/activate
easy_install -U pip
pip install --upgrade pip setuptools wheel
pip install --upgrade PySide2
pip install --upgrade xmltodict
pip install --upgrade hearthstone
pip install --upgrade hearthstone-data
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
