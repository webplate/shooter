# -*- mode: python -*-
#pyinstaller specification file for windows one exe packing

a = Analysis(['main.py'],
             pathex=['E:\\shooter'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          Tree('imgs', prefix='imgs'),
          Tree('fonts', prefix='fonts'),
          Tree('sounds', prefix='sounds'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='shooter.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
