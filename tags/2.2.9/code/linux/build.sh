#!/bin/sh
# 2007-09-20

pyinstallerPath=/home/mt/pyinstaller
dicPath=../dictionaries

echo "A script to build a Zeugs distribution package for Linux"
echo "using pyinstaller"
echo ""
echo "First ensure that the paths 'pyinstallerPath' and 'dicPath'"
echo "are set correctly:"
echo "     pyinstallerPath=${pyinstallerPath}"
echo "             dicPath=${dicPath}"
echo ""
echo "then run it as ./build.sh from its own directory."

# Folder 'dictionaries' contains the desired dictionaries, both '.aff'
# and '.dic' parts

python ${pyinstallerPath}/Configure.py
python ${pyinstallerPath}/Makespec.py zeugs.py
python ${pyinstallerPath}/Build.py zeugs-linux.spec

# The start script
cp zeugs.sh distzeugs

# Move the libraries to the lib folder (because of enchant otherwise
# having problems finding the dictionaries)
mkdir -p distzeugs/lib
mv distzeugs/libQt* distzeugs/lib

# Bodges (bits that pyinstaller doesn't manage)
enchantlib=$( ldd distzeugs/*enchant.so | grep enchant | cut -d' ' -f3 )
cp ${enchantlib} distzeugs/lib
edir=$( dirname ${enchantlib} )
mkdir -p distzeugs/lib/enchant
cp ${edir}/enchant/*myspell*.so distzeugs/lib/enchant
sqllib=$( ldd distzeugs/*sqlite3.so | grep sqlite | cut -d' ' -f3 )
cp ${sqllib} distzeugs/lib

# Dictionary stuff
mkdir -p distzeugs/share/enchant/myspell
cp -dp ${dicPath}/* distzeugs/share/enchant/myspell

# tar up the distribution directory
v=$( cat VERSION | sed 's/ //g' )
tar -czf zeugs-linux-${v}.tar.gz distzeugs
