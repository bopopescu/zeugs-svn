# setup.py for py2exe

#N.B.: I haven't got it working - it can't manage QtSvg
# pyInstaller seems more successful, though a bit more complicated ...

import os
from distutils.core import setup
import py2exe
import enchant

iconList = [os.path.join("icons", i) for i in os.listdir("icons")]
layouts = []
for l in os.walk("layouts"):
    if not l[2]: continue
    fl = [os.path.join(l[0], f) for f in l[2]]
    layouts.append((l[0], fl))

setup(windows=[{"script":"zeugs.py"}],
        options={"py2exe":{"includes":["sip"]}},
        data_files=(enchant.utils.win32_data_files()
                + [("icons", iconList),]
                + layouts
                + [("", ["C:\\Qt\\4.2.3\\bin\\QtSvg4.dll"]),]
            )
        )
