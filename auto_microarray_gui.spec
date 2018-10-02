# -*- mode: python -*-

block_cipher = None
options = [ ("v", None, "OPTION")]

a = Analysis(['auto_microarray\\auto_microarray_gui.py'],
             pathex=['D:\\grego\\Documents\\Pathology\\Projects\\biodiscovery', 'D:\\miniconda\\lib\\site-packages\\', 'D:\\miniconda\\lib\\site-packages\\auto_microarray'],
             #path['D:\\miniconda\\lib\\site-packages\\'],
             binaries=[],
             datas=[],
             hiddenimports=['auto_microarray', 'auto_microarray.validateAscessionNumber','pandas._libs.tslibs.timedeltas','pandas._libs.tslibs.nattype','pandas._libs.tslibs.np_datetime','pandas._libs.skiplist'],
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
          exclude_binaries=True,
          name='auto_microarray_gui',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='auto_microarray_gui')
