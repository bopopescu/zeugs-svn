REM A batch file for PyInstaller on Windows

REM Before the first use of PyInstaller it must be configured for the system
REM it is to be run on, e.g.:
REM     c:\python25\python Configure.py
REM (or else double-clicking on Configure.py should work)
REM A 'config.dat' file should be produced.

REM to use 'upx', place the file 'upx.exe' (from the zipped distribution) on
REM the PATH (e.g. in the python directory).
REM It could be that upx has to be on the PATH when Configure.py is run, so
REM that it is recognized by PyInstaller.

REM With PyInstaller version 1.3 an additional file is needed for PyQt4:
REM #   hooks\hook-PyQt4.py
REM hiddenimports = ['sip']

REM Place this batch file in a convenient directory together with your
REM source code and run it.

REM Here is the code!
set path=c:\python25;%path%
set PIP=c:\python25\pyinstaller-1.3\

REM Actually only necessary on the first run, but putting at here might
REM save confusion.
python %PIP%Configure.py


REM python %PIP%Makespec.py --onefile --noconsole --upx zeugs.py
REM python %PIP%Makespec.py --onedir --noconsole zeugs.py
python %PIP%Build.py zeugs.spec
