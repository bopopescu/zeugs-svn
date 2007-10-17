#!/bin/sh
# Starter script for the stand-alone linux package
thisapp=$( readlink -f $0 )
thisdir=$( dirname ${thisapp} )
cd ${thisdir}
LD_LIBRARY_PATH=${thisdir}/lib ${thisdir}/zeugs $1
