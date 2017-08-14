# -*- mode: python -*-

block_cipher = None


a = Analysis(['OpenDarkness.py'],
             pathex=['/Network/Servers/andoria.wi.uni-potsdam.de/Volumes/Homefiles 1/MA/KTauchert/Desktop/OpenDarkness/Mac'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          Tree('/Network/Servers/andoria.wi.uni-potsdam.de/Volumes/Homefiles 1/MA/KTauchert/Desktop/OpenDarkness/Mac/gui/images', prefix='gui/images/'),
          Tree('/Network/Servers/andoria.wi.uni-potsdam.de/Volumes/Homefiles 1/MA/KTauchert/Desktop/OpenDarkness/Mac/gui/filingarea', prefix='gui/filingarea/'),
          a.zipfiles,
          a.datas,
          name='OpenDarkness',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          version='version.txt')
app = BUNDLE(exe,
             name='OpenDarkness.app',
             icon='/Network/Servers/andoria.wi.uni-potsdam.de/Volumes/Homefiles 1/MA/KTauchert/Desktop/OpenDarkness/Mac/gui/images/OD_icon.ico',
             bundle_identifier=None)
