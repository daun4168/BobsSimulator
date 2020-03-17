cd ..
call venv/scripts/activate
easy_install -U pip
pip install --upgrade pip setuptools wheel
pip install PySide2
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
pip install xmltodict
pip install hearthstone
