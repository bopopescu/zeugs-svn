a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), 'zeugs.py'],
             pathex=['/home/mt/pyinstaller'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildzeugs-linux/zeugs',
          debug=False,
          strip=False,
          upx=False,
          console=1 )
coll = COLLECT( exe,
               a.binaries,
               [('VERSION', 'VERSION', 'DATA')],
               Tree('doc', 'doc/'),
               Tree('icons', 'icons/'),
               Tree('i18n','i18n/'),
               strip=False,
               upx=False,
               name='distzeugs')

