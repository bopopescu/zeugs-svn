# spec file for PyInstaller on Windows - see zeugs_PyI.bat
# This file was written based on the automatically generated zeugs.spec

a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'),
        os.path.join(HOMEPATH,'support\\useUnicode.py'), 'zeugs.py'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildzeugs/zeugs.exe',
          debug=False,
          strip=False,
          upx=False,
          console=False )

# change to console=True to get console

coll = COLLECT( exe,
               a.binaries,
               [('VERSION', 'VERSION', 'DATA')],
#               Tree('examples', 'examples\\'),
               Tree('doc', 'doc\\'),
               Tree('icons', 'icons\\'),
               Tree('i18n', 'i18n\\'),
               Tree('..\\dictionaries', 'share\\enchant\\myspell\\'),
               Tree('C:\\Python25\\lib\\site-packages\\enchant\\lib',
                    'lib\\'),
               strip=False,
               upx=False,
               name='distzeugs')
