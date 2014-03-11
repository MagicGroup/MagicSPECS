#!/bin/bash

# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.

[ -z "$OBJDUMP" ] && OBJDUMP=mingw-objdump

targets=$@
if [ -z "$targets" ] ; then
    echo "Usage: $0 [ mingw32 ] [ mingw64 ]"
    exit 1
fi

# Get the list of files.

filelist=`sed "s/['\"]/\\\&/g"`

dlls=$(echo $filelist | tr [:blank:] '\n' | grep -Ei '\.(dll|exe)$')
pkgconfig_files=$(echo $filelist | tr [:blank:] '\n' | grep -Ei '\.(pc)$')

for target in $targets; do
	dll_found=false
	host_triplet=`rpm --eval "%{${target}_target}"`
	for f in $dlls; do
		if [[ $f =~ .*$host_triplet.* ]]; then
			$OBJDUMP -p $f | grep 'DLL Name' | grep -Eio '[-._\+[:alnum:]]+\.dll' |
				tr [:upper:] [:lower:] |
				sed "s/\(.*\)/$target(\1)/"
			dll_found=true
		fi
	done

	# Add a dependency on filesystem and crt if necessary
	if [ $dll_found = true ]; then
		echo "${target}-filesystem >= 95"
		echo "${target}-crt"
	fi

	pkgconfig_files_found=false
	for f in $pkgconfig_files; do
		if [[ $f =~ .*$host_triplet.* ]]; then
			pkgconfig_files_found=true
		fi
	done

	# Add a dependency on $target-pkg-config if necessary
	if [ $pkgconfig_files_found = true ]; then
		echo "${target}-pkg-config"
	fi
done | sort -u
