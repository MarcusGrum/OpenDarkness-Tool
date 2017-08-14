# -*- mode: python -*-

block_cipher = None


a = Analysis(['OpenDarkness.py'],
             pathex=['D:\\uni_gits\\opendarkness\\code\\Win'],
             binaries=[],
             datas=[],
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
          Tree('D:\\uni_gits\\opendarkness\\code\\Win\\gui\\filingarea', prefix='gui\\filingarea\\'),
          Tree('D:\\uni_gits\\opendarkness\\code\\Win\\gui\\images',prefix='gui\\images'),
          a.zipfiles,
          a.datas,
          name='OpenDarkness',
          debug=False,
          strip=False,
          upx=False,
          console=False, version='version.txt',
          icon='D:\\uni_gits\\opendarkness\\code\\Win\\gui\\images\\OD_icon.ico')
