svn export https://edk2.svn.sourceforge.net/svnroot/edk2/trunk/edk2 edk2-svn$1
rm -rf edk2-svn$1/BaseTools/Bin
rm -rf edk2-svn$1/ShellBinPkg
rm -rf edk2-svn$1/FatBinPkg
tar -cv edk2-svn$1 | xz -6 > edk2-svn$1.tar.xz
