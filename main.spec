# -*- mode: python -*-
#pyinstaller specification file for windows one exe packing
#use it like :
#   python c:\pyinstaller\PyInstaller.py main.spec
#and put upx in path for compression

a = Analysis(['main.py'],
             pathex=['E:\\shooter'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

#remove unused modules
#~ a.binaries = [x for x in a.binaries if not x[0].startswith("tcl")]
#and eventualy single binaries
#~ a.binaries = a.binaries - TOC([('w9xpopen.exe', '', '')])
#remove warning
a.datas = [x for x in a.datas if not x[0].endswith("pyconfig.h")]

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
          console=False,#no i/o dos console
          icon='shooter.ico') 
