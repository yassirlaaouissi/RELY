# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['OneTimeScan.py'],
             pathex=['C:\\School\\Python\\RELY2'],
             binaries=[],
             datas=[('C:/Python37/Lib/site-packages/pyfiglet', './pyfiglet')],
             hiddenimports=['win32timezone'],
             hookspath=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='OneTimeScan',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
