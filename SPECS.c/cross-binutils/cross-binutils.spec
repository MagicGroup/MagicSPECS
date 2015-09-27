
%define cross cross
%define rpmprefix %{nil}

%define build_all		1
%define build_alpha		%{build_all}
%define build_arm		%{build_all}
%define build_aarch64		%{build_all}
%define build_avr32		%{build_all}
%define build_blackfin		%{build_all}
%define build_c6x		%{build_all}
%define build_cris		%{build_all}
%define build_frv		%{build_all}
%define build_h8300		%{build_all}
%define build_hppa		%{build_all}
%define build_hppa64		%{build_all}
%define build_ia64		%{build_all}
%define build_m32r		%{build_all}
%define build_m68k		%{build_all}
%define build_metag		%{build_all}
%define build_microblaze	%{build_all}
%define build_mips64		%{build_all}
%define build_mn10300		%{build_all}
%define build_nios2		%{build_all}
%define build_openrisc		%{build_all}
%define build_powerpc64		%{build_all}
%define build_s390x		%{build_all}
%define build_score		%{build_all}
%define build_sh		%{build_all}
%define build_sh64		%{build_all}
%define build_sparc64		%{build_all}
%define build_tile		%{build_all}
%define build_x86_64		%{build_all}
%define build_xtensa		%{build_all}

# 32-bit packages we don't build as we can use the 64-bit package instead
%define build_i386		0
%define build_mips		0
%define build_powerpc		0
%define build_s390		0
%define build_sparc		0
%define build_sh4		0

# not available in binutils-2.24
%define build_hexagon		0
%define build_unicore32		0

# BZ 1124342: Enable deterministic archives by default.
%define enable_deterministic_archives 1

Summary: A GNU collection of cross-compilation binary utilities
Name: %{cross}-binutils
Version: 2.25.1
Release: 2%{?dist}
License: GPLv3+
Group: Development/Tools
URL: http://sources.redhat.com/binutils

# Note - the Linux Kernel binutils releases are too unstable and contain too
# many controversial patches so we stick with the official FSF version
# instead.
Source: http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2

Source2: binutils-2.19.50.0.1-output-format.sed

# Bring up to date with what's in the git release branch
#Patch00: binutils-2.24-cde98f8566e14f52b896abc92c357cdd14717505.patch

Patch01: binutils-2.20.51.0.2-libtool-lib64.patch
Patch02: binutils-2.20.51.0.10-ppc64-pie.patch
Patch03: binutils-2.20.51.0.2-ia64-lib64.patch
Patch04: binutils-2.25-version.patch
Patch05: binutils-2.25-set-long-long.patch
Patch06: binutils-2.20.51.0.10-copy-osabi.patch
Patch07: binutils-2.20.51.0.10-sec-merge-emit.patch
# Enable -zrelro by default: BZ #621983
Patch08: binutils-2.22.52.0.1-relro-on-by-default.patch
# Local patch - export demangle.h with the binutils-devel rpm.
Patch09: binutils-2.22.52.0.1-export-demangle.h.patch
# Disable checks that config.h has been included before system headers.  BZ #845084
Patch10: binutils-2.22.52.0.4-no-config-h-check.patch
# Fix addr2line to use the dynamic symbol table if it could not find any ordinary symbols.
Patch11: binutils-2.23.52.0.1-addr2line-dynsymtab.patch
# Patch12: binutils-2.23.2-kernel-ld-r.patch
Patch12: binutils-2.25-kernel-ld-r.patch
# Correct bug introduced by patch 12
Patch13: binutils-2.23.2-aarch64-em.patch
# Fix detections little endian PPC shared libraries
Patch14: binutils-2.24-ldforcele.patch
# Fix parsing of corupt iHex binaries
Patch15: binutils-2.25.1-ihex-parsing.patch
# backport https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;h=e9c1bdad269c0c3352eebcc9481ed65144001b0b
# Qt linked with gold crash on startup, BZ #1193044
Patch16: binutils-2.25.1-dynamic_list.patch

# Fix formatless sprintfs in Score-specific code.
Patch100: cross-binutils-2.25-fixup-for-sh64.patch
Patch101: cross-binutils-2.25-fixup-microblaze.patch

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel
# BZ 920545: We need pod2man in order to build the manual pages.
BuildRequires: /usr/bin/pod2man
# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
Conflicts: gcc-c++ < 4.0.0
%ifarch ia64
Obsoletes: gnupro <= 1117-1
%endif
Provides: bundled(libiberty)

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

%package -n %{cross}-binutils-common
Summary: Cross-build binary utility documentation and translation files
Group: Development/Tools
BuildArch: noarch
%description -n %{cross}-binutils-common
Documentation, manual pages and translation files for cross-build binary image
generation, manipulation and query tools.

%define do_package() \
%if %2 \
%package -n %{rpmprefix}binutils-%1 \
Summary: Cross-build binary utilities for %1 \
Group: Development/Tools \
Requires: %{cross}-binutils-common == %{version}-%{release} \
%description -n %{rpmprefix}binutils-%1 \
Cross-build binary image generation, manipulation and query tools. \
%endif

%define do_symlink() \
%if %2 \
%package -n %{rpmprefix}binutils-%1 \
Summary: Cross-build binary utilities for %1 \
Group: Development/Tools \
Requires: binutils-%3 == %{version}-%{release} \
%description -n %{rpmprefix}binutils-%1 \
Cross-build binary image generation, manipulation and query tools. \
%endif

%do_package alpha-linux-gnu	%{build_alpha}
%do_package arm-linux-gnu	%{build_arm}
%do_package aarch64-linux-gnu	%{build_aarch64}
%do_package avr32-linux-gnu	%{build_avr32}
%do_package bfin-linux-gnu	%{build_blackfin}
%do_package c6x-linux-gnu	%{build_c6x}
%do_package cris-linux-gnu	%{build_cris}
%do_package frv-linux-gnu	%{build_frv}
%do_package h8300-linux-gnu	%{build_h8300}
%do_package hexagon-linux-gnu	%{build_hexagon}
%do_package hppa-linux-gnu	%{build_hppa}
%do_package hppa64-linux-gnu	%{build_hppa64}
%do_package i386-linux-gnu	%{build_i386}
%do_package ia64-linux-gnu	%{build_ia64}
%do_package m32r-linux-gnu	%{build_m32r}
%do_package m68k-linux-gnu	%{build_m68k}
%do_package metag-linux-gnu	%{build_metag}
%do_package microblaze-linux-gnu %{build_microblaze}
%do_package mips-linux-gnu	%{build_mips}
%do_package mips64-linux-gnu	%{build_mips64}
%do_package mn10300-linux-gnu	%{build_mn10300}
%do_package nios2-linux-gnu	%{build_nios2}
%do_package openrisc-linux-gnu	%{build_openrisc}	or1k-linux-gnu
%do_package powerpc-linux-gnu	%{build_powerpc}
%do_package powerpc64-linux-gnu	%{build_powerpc64}
%do_symlink ppc-linux-gnu	%{build_powerpc}	powerpc-linux-gnu
%do_symlink ppc64-linux-gnu	%{build_powerpc64}	powerpc64-linux-gnu
%do_package s390-linux-gnu	%{build_s390}
%do_package s390x-linux-gnu	%{build_s390x}
%do_package score-linux-gnu	%{build_score}
%do_package sh-linux-gnu	%{build_sh}
%do_package sh4-linux-gnu	%{build_sh4}
%do_package sh64-linux-gnu	%{build_sh64}
%do_package sparc-linux-gnu	%{build_sparc}
%do_package sparc64-linux-gnu	%{build_sparc64}
%do_package tile-linux-gnu	%{build_tile}
%do_package unicore32-linux-gnu	%{build_unicore32}
%do_package x86_64-linux-gnu	%{build_x86_64}
%do_package xtensa-linux-gnu	%{build_xtensa}

# Where the binaries aimed at gcc will live (ie. /usr/<target>/bin/)
%define auxbin_prefix %{_exec_prefix}

###############################################################################
#
# Preparation
#
###############################################################################
%prep

%define srcdir binutils-%{version}
%setup -q -n %{srcdir} -c
cd %{srcdir}
%if 1
#%patch00 -p1 -b .latest-git~
%patch01 -p1 -b .libtool-lib64~
%patch02 -p1 -b .ppc64-pie~
%ifarch ia64
%if "%{_lib}" == "lib64"
%patch03 -p1 -b .ia64-lib64~
%endif
%endif
%patch04 -p1 -b .version~
%patch05 -p1 -b .set-long-long~
%patch06 -p1 -b .copy-osabi~
%patch07 -p1 -b .sec-merge-emit~
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch08 -p1 -b .relro~
%endif
%patch09 -p1 -b .export-demangle-h~
%patch10 -p1 -b .no-config-h-check~
%patch11 -p1 -b .addr2line~
%patch12 -p1 -b .kernel-ld-r~
%patch13 -p1 -b .aarch64~
%patch14 -p1 -b .ldforcele~
%patch15 -p1 -b .ihex~
%patch16 -p1 -b .dynamic_list~
%endif

%patch100 -p1 -b .sh64-fixup~
%patch101 -p1 -b .microblaze-fixup~

# We cannot run autotools as there is an exact requirement of autoconf-2.59.

# On ppc64 and aarch64, we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c
sed -i -e '/common_pagesize/s/4 /64 /' gold/powerpc.cc
sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc
# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi
# $PACKAGE is used for the gettext catalog name.
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{cross}-/' */configure
# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done
touch */configure

function prep_target () {
    target=$1
    cond=$2

    if [ $cond != 0 ]
    then
	echo $1 >&5
    fi
}

cd ..
(
    prep_target alpha-linux-gnu		%{build_alpha}
    prep_target arm-linux-gnu		%{build_arm}
    prep_target aarch64-linux-gnu	%{build_aarch64}
    prep_target avr32-linux-gnu		%{build_avr32}
    prep_target bfin-linux-gnu		%{build_blackfin}
    prep_target c6x-linux-gnu		%{build_c6x}
    prep_target cris-linux-gnu		%{build_cris}
    prep_target frv-linux-gnu		%{build_frv}
    prep_target h8300-linux-gnu		%{build_h8300}
    prep_target hexagon-linux-gnu	%{build_hexagon}
    prep_target hppa-linux-gnu		%{build_hppa}
    prep_target hppa64-linux-gnu	%{build_hppa64}
    prep_target i386-linux-gnu		%{build_i386}
    prep_target ia64-linux-gnu		%{build_ia64}
    prep_target m32r-linux-gnu		%{build_m32r}
    prep_target m68k-linux-gnu		%{build_m68k}
    prep_target metag-linux-gnu		%{build_metag}
    prep_target microblaze-linux-gnu	%{build_microblaze}
    prep_target mips-linux-gnu		%{build_mips}
    prep_target mips64-linux-gnu	%{build_mips64}
    prep_target mn10300-linux-gnu	%{build_mn10300}
    prep_target nios2-linux-gnu		%{build_nios2}
    prep_target openrisc-linux-gnu	%{build_openrisc}
    prep_target powerpc-linux-gnu	%{build_powerpc}
    prep_target powerpc64-linux-gnu	%{build_powerpc64}
    prep_target s390-linux-gnu		%{build_s390}
    prep_target s390x-linux-gnu		%{build_s390x}
    prep_target score-linux-gnu		%{build_score}
    prep_target sh-linux-gnu		%{build_sh}
    prep_target sh4-linux-gnu		%{build_sh4}
    prep_target sh64-linux-gnu		%{build_sh64}
    prep_target sparc-linux-gnu		%{build_sparc}
    prep_target sparc64-linux-gnu	%{build_sparc64}
    prep_target tile-linux-gnu		%{build_tile}
    prep_target unicore32-linux-gnu	%{build_unicore32}
    prep_target x86_64-linux-gnu	%{build_x86_64}
    prep_target xtensa-linux-gnu	%{build_xtensa}
) 5>target.list

n=0
for target in `cat target.list`
do
    n=1
    break
done
if [ $n = 0 ]
then
    echo "No targets selected" >&2
    exit 8
fi

###############################################################################
#
# Build
#
###############################################################################
%build

function config_target () {
    arch=$1
    prefix=$arch-
    build_dir=${1%%%%-*}

    case $arch in
	arm-*)		target=arm-linux-gnueabi;;
	aarch64-*)	target=aarch64-linux-gnu;;
	avr32-*)	target=avr-linux;;
	bfin-*)		target=bfin-uclinux;;
	c6x-*)		target=c6x-uclinux;;
	h8300-*)	target=h8300-elf;;
	m32r-*)		target=m32r-elf;;
	mn10300-*)	target=am33_2.0-linux;;
	m68knommu-*)	target=m68k-linux;;
	openrisc-*)	target=or1k-linux-gnu;;
	parisc-*)	target=hppa-linux;;
	score-*)	target=score-elf;;
	sh64-*)		target=sh64-linux-elf;;
	tile-*)		target=tilegx-linux;;
	v850-*)		target=v850e-linux;;
	x86-*)		target=x86_64-linux;;
	*)		target=$arch;;
    esac

    echo $arch: target is $target
    export CFLAGS="$RPM_OPT_FLAGS"
    CARGS=

    case $target in i?86*|sparc*|ppc*|powerpc*|s390*|sh*|arm*)
	    CARGS="$CARGS --enable-64-bit-bfd"
	    ;;
    esac

    case $target in ia64*)
	    CARGS="$CARGS --enable-targets=i386-linux"
	    ;;
    esac

    case $target in ppc*|powerpc*)
	    CARGS="$CARGS --enable-targets=spu,powerpc-linux,ppc64le-linux-gnu,ppcle-linux-gnu"
	    ;;
    esac

    case $target in sh-*)
	    CARGS="$CARGS --enable-targets=sh4-linux,sh-elf,sh-linux"
	    ;;
    esac

    mkdir $build_dir
    cd $build_dir

    # We could optimize the cross builds size by --enable-shared but the produced
    # binaries may be less convenient in the embedded environment.
    LDFLAGS='-Wl,-z,relro ' \
    ../%{srcdir}/configure \
	--disable-dependency-tracking \
	--disable-silent-rules \
	--enable-checking \
	--prefix=%{_prefix} \
	--exec-prefix=%{auxbin_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=$target \
	--program-prefix=$prefix \
	--disable-shared \
	--disable-install_libbfd \
	--with-sysroot=%{_prefix}/$arch/sys-root \
	$CARGS \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla/
    cd ..
}

for target in `cat target.list`
do
    config_target $target
done

function build_target () {
    build_dir=${1%%%%-*}
    make -C $build_dir %{_smp_mflags} tooldir=%{_prefix} all
}

for target in `cat target.list`
do
    build_target $target
done

# for documentation purposes only
mkdir %{cross}-binutils
cd %{cross}-binutils
../%{srcdir}/configure \
    --disable-dependency-tracking \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --exec-prefix=%{auxbin_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --program-prefix=%{cross}- \
    --disable-shared \
    --with-bugurl=http://bugzilla.redhat.com/bugzilla/
make %{_smp_mflags} tooldir=%{_prefix} all
cd ..

###############################################################################
#
# Installation
#
###############################################################################
%install
rm -rf %{buildroot}

function install_bin () {
    cpu=${1%%%%-*}
    build_dir=$cpu
    make install -C $build_dir DESTDIR=%{buildroot}

    # We want links for ppc and ppc64 also if we make powerpc or powerpc64
    case $cpu in
	powerpc*)
	    cd %{buildroot}/usr/bin
	    for i in $cpu-*
	    do
		ln -s $i ppc${i#powerpc}
	    done
	    cd -
	    cd %{buildroot}/usr/
	    for i in $cpu-*
	    do
		ln -s $i ppc${i#powerpc}
	    done
	    cd -
	    cd %{buildroot}/usr/share/man/man1
	    for i in $cpu-*
	    do
		ln -s $i ppc${i#powerpc}
	    done
	    cd -
	    ;;
    esac
}

for target in `cat target.list`
do
    echo "=== INSTALL target $target ==="
    mkdir -p %{buildroot}%{_prefix}/$target/sys-root
    install_bin $target

#    if [ $target = sh64-linux-gnu ]
#    then
#	ln -s %{auxbin_prefix}/sh64-elf %{buildroot}%{auxbin_prefix}/sh64-linux
#    fi
done

echo "=== INSTALL man targets ==="
make install-man1 -C %{cross}-binutils/binutils/doc DESTDIR=%{buildroot}
make install-man1 -C %{cross}-binutils/gas/doc DESTDIR=%{buildroot}
make install-man1 -C %{cross}-binutils/ld DESTDIR=%{buildroot}
make install-man1 -C %{cross}-binutils/gprof DESTDIR=%{buildroot}

echo "=== INSTALL po targets ==="
make install -C %{cross}-binutils/binutils/po DESTDIR=%{buildroot}
make install -C %{cross}-binutils/gas/po DESTDIR=%{buildroot}
make install -C %{cross}-binutils/ld/po DESTDIR=%{buildroot}
make install -C %{cross}-binutils/gprof/po DESTDIR=%{buildroot}
make install -C %{cross}-binutils/bfd/po DESTDIR=%{buildroot}
make install -C %{cross}-binutils/opcodes/po DESTDIR=%{buildroot}

# Add the additional symlink-only targets
grep ^powerpc target.list | sed -e s/powerpc/ppc/ >symlink-target.list
cat symlink-target.list >>target.list

# For cross-binutils we drop the documentation.
echo "=== REMOVE documentation ==="
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_infodir}/dir

echo "=== REMOVE libraries and scripts ==="
rm -rf %{buildroot}%{_libdir}/libiberty.a
rm -rf %{buildroot}%{auxbin_prefix}/*/lib/ldscripts
rmdir %{buildroot}%{auxbin_prefix}/*/lib || :

echo "=== BUILD file lists ==="
function build_file_list () {
    arch=$1
    cpu=${arch%%%%-*}

    case $cpu in
	avr32)		target_cpu=avr;;
	bfin)		target_cpu=bfin;;
	h8300)		target_cpu=h8300;;
	mn10300)	target_cpu=am33_2.0;;
	openrisc)	target_cpu=or1k;;
	score)		target_cpu=score;;
	tile)		target_cpu=tilegx;;
	v850)		target_cpu=v850e;;
	*)		target_cpu=$cpu;;
    esac

    (
	echo %{_bindir}/$arch-[!l]\*
	echo %{_bindir}/$arch-ld\*
	if [ -L %{buildroot}%{auxbin_prefix}/$target_cpu-* ]
	then
	    echo %{auxbin_prefix}/$target_cpu-*
	else
	    echo %{auxbin_prefix}/$target_cpu-*/bin/\*
	fi
	echo %{_mandir}/man1/$arch-\*
	echo '%%attr(0755,root,root)' %{_prefix}/$arch/sys-root
    ) >files.$arch
}

for target in `cat target.list`
do
    build_file_list $target
done

# All the installed manual pages and translation files for each program are the
# same, so symlink them to the core package
echo "=== CROSSLINK man pages ==="
cd %{buildroot}%{_mandir}/man1
for i in %{cross}-*.1*
do
    j=${i#%{cross}-}

    for k in *-$j
    do
	if [ $k != $i ]
	then
	    ln -sf $i $k
	fi
    done
done


# Add ld.bfd manual pages
find * -name "*ld.1*" -a ! -name "%{cross}-ld.1*" -print |
while read x
do
    y=`echo $x | sed -e s/ld[.]1/ld.bfd.1/`
    ln -s $x $y
done

cd -

# Find the language files which only exist in the common package
(
    %find_lang %{cross}-binutils
    %find_lang %{cross}-opcodes
    %find_lang %{cross}-bfd
    %find_lang %{cross}-gas
    %find_lang %{cross}-ld
    %find_lang %{cross}-gprof
    cat %{cross}-binutils.lang
    cat %{cross}-opcodes.lang
    cat %{cross}-bfd.lang
    cat %{cross}-gas.lang
    cat %{cross}-ld.lang
    cat %{cross}-gprof.lang
) >files.cross



###############################################################################
#
# Cleanup
#
###############################################################################
%clean
rm -rf %{buildroot}

###############################################################################
#
# Filesets
#
###############################################################################
%files -n %{cross}-binutils-common -f files.cross
%doc %{srcdir}/README
%doc %{srcdir}/COPYING*
%{_mandir}/man1/%{cross}-*

%define do_files() \
%if %2 \
%files -n %{rpmprefix}binutils-%1 -f files.%1 \
%endif

%do_files alpha-linux-gnu	%{build_alpha}
%do_files arm-linux-gnu		%{build_arm}
%do_files aarch64-linux-gnu	%{build_aarch64}
%do_files avr32-linux-gnu	%{build_avr32}
%do_files bfin-linux-gnu	%{build_blackfin}
%do_files c6x-linux-gnu		%{build_c6x}
%do_files cris-linux-gnu	%{build_cris}
%do_files frv-linux-gnu		%{build_frv}
%do_files h8300-linux-gnu	%{build_h8300}
%do_files hexagon-linux-gnu	%{build_hexagon}
%do_files hppa-linux-gnu	%{build_hppa}
%do_files hppa64-linux-gnu	%{build_hppa64}
%do_files i386-linux-gnu	%{build_i386}
%do_files ia64-linux-gnu	%{build_ia64}
%do_files m32r-linux-gnu	%{build_m32r}
%do_files m68k-linux-gnu	%{build_m68k}
%do_files metag-linux-gnu	%{build_metag}
%do_files microblaze-linux-gnu	%{build_microblaze}
%do_files mips-linux-gnu	%{build_mips}
%do_files mips64-linux-gnu	%{build_mips64}
%do_files mn10300-linux-gnu	%{build_mn10300}
%do_files nios2-linux-gnu	%{build_nios2}
%do_files openrisc-linux-gnu	%{build_openrisc}
%do_files powerpc-linux-gnu	%{build_powerpc}
%do_files powerpc64-linux-gnu	%{build_powerpc64}
%do_files ppc-linux-gnu		%{build_powerpc}
%do_files ppc64-linux-gnu	%{build_powerpc64}
%do_files s390-linux-gnu	%{build_s390}
%do_files s390x-linux-gnu	%{build_s390x}
%do_files score-linux-gnu	%{build_score}
%do_files sh-linux-gnu		%{build_sh}
%do_files sh4-linux-gnu		%{build_sh4}
%do_files sh64-linux-gnu	%{build_sh64}
%do_files sparc-linux-gnu	%{build_sparc}
%do_files sparc64-linux-gnu	%{build_sparc64}
%do_files tile-linux-gnu	%{build_tile}
%do_files unicore32-linux-gnu	%{build_unicore32}
%do_files x86_64-linux-gnu	%{build_x86_64}
%do_files xtensa-linux-gnu	%{build_xtensa}

%changelog
* Sat Sep 26 2015 Liu Di <liudidi@gmail.com> - 2.25.1-2
- 为 Magic 3.0 重建

* Mon Aug 24 2015 David Howells <dhowells@redhat.com> - 2.25.1-1
- Sync with binutils-2.25.1-4.
- Set --enable-targets if the target is powerpc* not just ppc*.
- Provide LE ppc and ppc64 emulations [BZ 1255947].

* Mon Apr 6 2015 David Howells <dhowells@redhat.com> - 2.25-4
- Microblaze: Fix extra-large constant handling [binutils bz 18189].

* Wed Jan 7 2015 David Howells <dhowells@redhat.com> - 2.25-3
- Fix up the target for SH64 and cease mixing 32-bit SH targets with SH64.
- SH64: Work around flags not getting set on incremental link of .a into .o [binutils bz 17288].

* Mon Jan 5 2015 David Howells <dhowells@redhat.com> - 2.25-1
- Sync with binutils-2.25 to pick up fixes.
  Resolves: BZ #1162577, #1162601, #1162611, #1162625

* Thu Nov 13 2014 David Howells <dhowells@redhat.com> - 2.24-7
- Fix problems with the ar program reported in FSF PR 17533.
  Resolves: BZ #1162672, #1162659

* Wed Nov 12 2014 David Howells <dhowells@redhat.com> - 2.24-6
- Sync with binutils to pick up fixes.
- Backport binutils 2.4 upstream branch to pick up more fixes.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 David Howells <dhowells@redhat.com> - 2.24-5
- Add NIOS2 arch support.

* Mon Jun 16 2014 David Howells <dhowells@redhat.com> - 2.24-4
- Fix gcc-4.9 new compile error in m68k handler in gas.

* Wed Jun 11 2014 David Howells <dhowells@redhat.com> - 2.24-4
- Sync with binutils-2.24-15 fixing the bfd_set_section_alignment() error [BZ 1106093]
- Apply the changes on binutils-2_24-branch in git to cab6c3ee9785f072a373afe31253df0451db93cf.

* Fri Mar 28 2014 David Howells <dhowells@redhat.com> - 2.24-2
- A sysroot of / is bad, so make it /usr/<program-prefix>/sys-root/.

* Thu Mar 27 2014 David Howells <dhowells@redhat.com> - 2.24-1
- Fix formatless sprintfs in Score.

* Wed Mar 26 2014 David Howells <dhowells@redhat.com> - 2.24-1
- Update to binutils-2.24-1.
- Add metag arch support.

* Fri Aug 9 2013 David Howells <dhowells@redhat.com> - 2.23.88.0.1-2
- Fix a build error in xtensa

* Thu Aug 8 2013 David Howells <dhowells@redhat.com> - 2.23.88.0.1-2
- Backport S390 .machinemode pseudo-op support from binutils-2.23.88.0.1-10.
- Add pod2man as a build requirement.

* Tue Jun 4 2013 David Howells <dhowells@redhat.com> - 2.23.88.0.1-1
- Update to binutils-2.22.88.0.1 to fix F19 texinfo issues [BZ 912921].

* Tue Jun 4 2013 David Howells <dhowells@redhat.com> - 2.23.51.0.3-2
- Backport cleanups from the RHEL-6.4 cross-compiler.
- Backport some macroisation from the RHEL-6.4 cross-compiler.
- The hppa64 target cannot actually build hppa, so provide hppa [BZ 892220].

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.51.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 2 2012 David Howells <dhowells@redhat.com> - 2.23.51.0.3-1
- Update to binutils-2.23.51.0.3.
- Added support for aarch64.

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 2.22.52.0.3-4
- Provides: bundled(libiberty)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.52.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Dan Horák <dan[at]danny.cz> - 2.22.52.0.3-2
- don't install libbfd/libopcode when host == target (eg. on s390x)

* Wed May 30 2012 David Howells <dhowells@redhat.com> - 2.22.52.0.3-1
- Update to binutils-2.22.52.0.3.
- Fixed a warning in the assembler for h8300 that caused the build to fail.

* Thu Mar 22 2012 David Howells <dhowells@redhat.com> - 2.22.52.0.1-8.1
- Initial import of cross-binutils [BZ 761619].

* Wed Mar 07 2012 Jakub Jelinek <jakub@redhat.com> - 2.22.52.0.1-8
- Fix up handling of hidden ifunc relocs on x86_64
- Add Intel TSX support
