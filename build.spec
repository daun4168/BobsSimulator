# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['BobsSimulator\\__init__.py'],
             pathex=['./'],
             binaries=[],
             datas=[('res', 'res'), ('BobsSimulator/logging.json', 'BobsSimulator'), ('venv/Lib/site-packages/hearthstone_data', 'hearthstone_data')],
             hiddenimports=['hearthstone', 'hearthstone_data'],
             hookspath=['BobsSimulator/hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='output',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='res\\app.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='output')