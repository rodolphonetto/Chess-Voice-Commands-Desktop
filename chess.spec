# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['chess.py'],
             pathex=['C:\\Users\\Rodolpho\\Desktop\\chess_voice'],
             binaries=[],
             datas=[('C:\\Users\\Rodolpho\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\vosk', './vosk')],
             hiddenimports=[],
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
          name='chess',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
