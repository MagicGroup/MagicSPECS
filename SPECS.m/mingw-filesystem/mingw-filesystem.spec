%global debug_package %{nil}

# Place RPM macros in %%{_rpmconfigdir}/macros.d if it exists (RPM 4.11+)
# Otherwise, use %%{_sysconfdir}/rpm
# https://lists.fedoraproject.org/pipermail/devel/2014-January/195026.html
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           mingw-filesystem
Version:        99
Release:        6%{?dist}
Summary:        MinGW cross compiler base filesystem and environment
Summary(zh_CN.UTF-8): MinGW 交叉编译器的基本文件系统和环境

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPLv2+
URL:            http://fedoraproject.org/wiki/MinGW
BuildArch:      noarch

Source0:        COPYING
Source1:        macros.mingw
Source2:        macros.mingw32
Source3:        macros.mingw64
Source4:        mingw32.sh
Source5:        mingw64.sh
Source6:        mingw-find-debuginfo.sh
Source7:        mingw-find-requires.sh
Source8:        mingw-find-provides.sh
Source9:        mingw-scripts.sh
Source10:       mingw-rpmlint.config
Source11:       Toolchain-mingw32.cmake
Source12:       Toolchain-mingw64.cmake
Source13:       mingw-find-lang.sh
Source14:       mingw32.attr
Source15:       mingw64.attr
# generated with:
# (rpm -ql mingw32-crt | grep '\.a$' | while read f ; do i686-w64-mingw32-dlltool   -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-mingw32
Source16:       standard-dlls-mingw32
# (rpm -ql mingw64-crt | grep '\.a$' | while read f ; do x86_64-w64-mingw32-dlltool -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-mingw64
Source17:       standard-dlls-mingw64

# Taken from the Fedora filesystem package
Source101:      https://fedorahosted.org/filesystem/browser/lang-exceptions
Source102:      iso_639.sed
Source103:      iso_3166.sed

BuildRequires:  iso-codes


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW

%description -l zh_CN.UTF-8
这个包包括了所有 MinGW 包需要的基本文件系统结构，RPM 宏定义和环境。

%package base
Summary:        Generic files which are needed for both mingw32-filesystem and mingw64-filesystem
Summary(zh_CN.UTF-8): mingw32-filesystem 和 mingw64-filesystem 共同需要的文件

# Obsolete the packages from the test repo
Obsoletes:      cross-filesystem < 67-2
Obsoletes:      cross-filesystem-scripts < 67-2
Obsoletes:      mingw-filesystem < 75-2
Obsoletes:      mingw-filesystem-scripts < 75-2

%description base
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW

%description base -l zh_CN.UTF-8
mingw32-filesystem 和 mingw64-filesystem 共同需要的文件。

%package -n mingw32-filesystem
Summary:        MinGW cross compiler base filesystem and environment for the win32 target
Summary(zh_CN.UTF-8): win32 目标系统需要基本文件系统和环境
Requires:       %{name}-base = %{version}-%{release}

# Note about 'Provides: mingw32(foo.dll)'
# ------------------------------------------------------------
#
# We want to be able to build & install mingw32 libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the mingw toolchain to develop software (ie. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
Provides:       %(sed "s/\(.*\)/mingw32(\1) /g" %{SOURCE16} | tr "\n" " ")
Provides:       mingw32(mscoree.dll)

%description -n mingw32-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW

%description -n mingw32-filesystem -l zh_CN.UTF-8
win32 目标系统需要基本文件系统和环境。

%package -n mingw64-filesystem
Summary:        MinGW cross compiler base filesystem and environment for the win64 target
Summary(zh_CN.UTF-8): win64 目标系统需要基本文件系统和环境
Requires:       %{name}-base = %{version}-%{release}

Provides:       %(sed "s/\(.*\)/mingw64(\1) /g" %{SOURCE17} | tr "\n" " ")
Provides:       mingw64(mscoree.dll)

%description -n mingw64-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW

%description -n mingw64-filesystem -l zh_CN.UTF-8
win64 目标系统需要基本文件系统和环境。

%prep
%setup -q -c -T
cp %{SOURCE0} COPYING


%build
# nothing


%install
mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{_libexecdir}/mingw-scripts

mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
for i in mingw32-configure mingw32-cmake mingw32-make mingw32-pkg-config \
         mingw64-configure mingw64-cmake mingw64-make mingw64-pkg-config ; do
  ln -s %{_libexecdir}/mingw-scripts $i
done
popd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{macrosdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{macrosdir}/macros.mingw
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{macrosdir}/macros.mingw32
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{macrosdir}/macros.mingw64

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint/

# Create the folders required for gcc and binutils
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/lib

# The MinGW system root which will contain Windows native binaries
# and Windows-specific header files, pkgconfig, etc.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/etc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/include/sys
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/lib/cmake
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/sbin

mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/etc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/lib/cmake
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/sbin

# We don't normally package manual pages and info files, except
# where those are not supplied by a Fedora native package.  So we
# need to create the directories.
#
# Note that some packages try to install stuff in
#   /usr/x86_64-pc-mingw32/sys-root/man and
#   /usr/x86_64-pc-mingw32/sys-root/doc
# but those are both packaging bugs.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/aclocal
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/themes
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/cmake
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/locale
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-w64-mingw32/sys-root/mingw/share/xml

mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/aclocal
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/themes
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/cmake
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/locale
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/xml

# Own folders for all locales
# Snippet taken from the Fedora filesystem package
sed -n -f %{SOURCE102} /usr/share/xml/iso-codes/iso_639.xml > $RPM_BUILD_ROOT/iso_639.tab
sed -n -f %{SOURCE103} /usr/share/xml/iso-codes/iso_3166.xml > $RPM_BUILD_ROOT/iso_3166.tab

grep -v "^$" $RPM_BUILD_ROOT/iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue

    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale}) %{_prefix}/i686-w64-mingw32/sys-root/mingw/share/locale/${locale}" >> filelist_mingw32
    echo "%lang(${locale}) %{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/locale/${locale}" >> filelist_mingw64
done

cat %{SOURCE101} | grep -v "^#" | grep -v "^$" | while read loc ; do
    locale=$loc
    locality=
    special=
    [[ "$locale" =~ "@" ]] && locale=${locale%%%%@*}
    [[ "$locale" =~ "_" ]] && locality=${locale##*_}
    [[ "$locality" =~ "." ]] && locality=${locality%%%%.*}
    [[ "$loc" =~ "_" ]] || [[ "$loc" =~ "@" ]] || special=$loc

    # If the locality is not official, skip it
    if [ -n "$locality" ]; then
        grep -q "^$locality" $RPM_BUILD_ROOT/iso_3166.tab || continue
    fi
    # If the locale is not official and not special, skip it
    if [ -z "$special" ]; then
        egrep -q "[[:space:]]${locale%%_*}[[:space:]]" $RPM_BUILD_ROOT/iso_639.tab || continue
    fi
    echo "%lang(${locale}) %{_prefix}/i686-w64-mingw32/sys-root/mingw/share/locale/${loc}" >> filelist_mingw32
    echo "%lang(${locale}) %{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/locale/${loc}" >> filelist_mingw64
done

rm -f $RPM_BUILD_ROOT/iso_639.tab
rm -f $RPM_BUILD_ROOT/iso_3166.tab

cat filelist_mingw32 filelist_mingw64 | grep "locale" | while read a b ; do
    mkdir -p -m 755 %{buildroot}/$b/LC_MESSAGES
done

# NB. NOT _libdir
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_rpmconfigdir}
install -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_rpmconfigdir}
install -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_rpmconfigdir}
install -m 0755 %{SOURCE13} $RPM_BUILD_ROOT%{_rpmconfigdir}

mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm/fileattrs
install -m 0644 %{SOURCE14} $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs/
install -m 0644 %{SOURCE15} $RPM_BUILD_ROOT%{_rpmconfigdir}/fileattrs/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mingw
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/mingw/
install -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/mingw/
magic_rpm_clean.sh

%files base
%doc COPYING
%dir %{_sysconfdir}/rpmlint/
%config(noreplace) %{_sysconfdir}/rpmlint/mingw-rpmlint.config
%{macrosdir}/macros.mingw
%{_libexecdir}/mingw-scripts
%{_rpmconfigdir}/mingw*
%dir %{_datadir}/mingw/

%files -n mingw32-filesystem
%{macrosdir}/macros.mingw32
%config(noreplace) %{_sysconfdir}/profile.d/mingw32.sh
%{_bindir}/mingw32-configure
%{_bindir}/mingw32-cmake
%{_bindir}/mingw32-make
%{_bindir}/mingw32-pkg-config
%{_prefix}/i686-w64-mingw32
%{_rpmconfigdir}/fileattrs/mingw32.attr
%{_datadir}/mingw/Toolchain-mingw32.cmake

%files -n mingw64-filesystem
%{macrosdir}/macros.mingw64
%config(noreplace) %{_sysconfdir}/profile.d/mingw64.sh
%{_bindir}/mingw64-configure
%{_bindir}/mingw64-cmake
%{_bindir}/mingw64-make
%{_bindir}/mingw64-pkg-config
%{_prefix}/x86_64-w64-mingw32
%{_rpmconfigdir}/fileattrs/mingw64.attr
%{_datadir}/mingw/Toolchain-mingw64.cmake


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 99-6
- 为 Magic 3.0 重建

* Mon Oct 13 2014 Liu Di <liudidi@gmail.com> - 99-5
- 为 Magic 3.0 重建

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 99-4
- Place the RPM macros in /usr/lib/rpm/macros.d when using a modern RPM

* Sat Aug  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 99-3
- Own the folders %%{mingw32_libdir}/cmake and %%{mingw64_libdir}/cmake
- Own all the locale folders below %%{mingw32_datadir}/locale and %%{mingw64_datadir}/locale (RHBZ #798329)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Kalev Lember <kalevlember@gmail.com> - 99-1
- Remove invalid macros with '++' in the name

* Sun Jun  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 98-2
- Only set the environment variable PKG_CONFIG_LIBDIR when
  using the macros %%mingw32_cmake, %%mingw32_cmake_kde4,
  %%mingw64_cmake or %%mingw64_cmake_kde4
- Fixes FTBFS of the mingw-matahari package

* Sun May 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 98-1
- Removed the use of the environment variable PKG_CONFIG_LIBDIR
  While building binaries the tool {i686,x86_64}-w64-mingw32-pkg-config
  should be used to find out pkg-config information
  The environment variable PKG_CONFIG already automatically points
  to the right cross-compiler aware version of pkg-config when
  the mingw{32,64}-pkg-config packages are installed
- Fixes compilation of mingw-gtk3 3.9.0 (GNOME BZ #699690)
- Automatically add R: mingw{32,64}-pkg-config tags when .pc files
  are detected while building mingw packages
- Bumped the minimum required version of mingw{32,64}-filesystem
  to >= 95 in built mingw packages as this is the first version of
  which was introduced in Fedora with a stable interface
- Updated the list of DLLs which are part of the Win32 API with
  the libraries d3dcompiler_46.dll, d3dcsx_46.dll, davclnt.dll,
  devmgr.dll, devobj.dll and devrtl.dll

* Thu Feb 28 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 97-3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).
- Minor spec fixes.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 16 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 97-1
- Added support for using the environment variables MINGW32_MAKE_ARGS and
  MINGW64_MAKE_ARGS. These environment variables can be used to  provide
  additional target-specific arguments when using the %%mingw_make macro

* Mon Dec  3 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 96-3
- Added support for RHEL6

* Sat Nov 10 2012 Kalev Lember <kalevlember@gmail.com> - 96-2
- Add provides for mscoree.dll and regenerate the standard-dlls file

* Mon Sep 17 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 96-1
- Added new macros for Qt5 support, %%mingw32_qmake_qt5, %%mingw64_qmake_qt5,
  %%mingw_qmake_qt4 and %%mingw_qmake_qt5
- It isn't necessary to call %%mingw32_env / %%mingw64_env any more
  in the %%mingw32_qmake_qt4 and %%mingw64_qmake_qt4 macros

* Mon Aug 13 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-14
- Fix the handling of quoted arguments in the cmake macros

* Tue Jul 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-13
- Make sure the %%mingw_cmake and %%mingw_cmake_kde4 macros respect the
  environment variable MINGW_BUILDDIR_SUFFIX

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 95-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Kalev Lember <kalevlember@gmail.com> - 95-11
- Fix syntax error in mingw64_env macro, thanks to Akira TAGOH (#831534)

* Wed Jun  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-10
- Prevent errors when the folders %%{mingw32_prefix} or %%{mingw64_prefix} are missing
- Fix parse error when -config files containing a . are available
  in %%{mingw32_bindir} or %%{mingw64_bindir} (RHBZ #657478)

* Thu Apr 19 2012 Kalev Lember <kalevlember@gmail.com> - 95-9
- Fix whitespace handling in %%mingw_configure and friends

* Sat Mar 17 2012 Kalev Lember <kalevlember@gmail.com> - 95-8
- Generate the list of mingw32(...) and mingw64(...) DLL name provides from
  mingw-crt import libraries

* Sat Mar 17 2012 Kalev Lember <kalevlember@gmail.com> - 95-7
- Define mingw_build_win32/win64 in system macros, so that each
  individual package wouldn't have to

* Fri Mar 16 2012 Kalev Lember <kalevlember@gmail.com> - 95-6
- Fix warnings during debuginfo generation

* Fri Mar 16 2012 Kalev Lember <kalevlember@gmail.com> - 95-5
- Simplify the mingw_make_install macro, also moving it to the deprecated
  section

* Mon Mar 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-4
- Added a manual provides for the native windows library ksuser.dll as
  wine doesn't have an implementation for this library at the moment

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 95-3
- Merge copy-n-paste duplicate %%mingw32_debug_package code
- Get rid of the USE_OLD_METHOD hack in mingw-find-debuginfo.sh
- Add missing %%mingw32_debug_install_post

* Tue Feb 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-2
- Fixed broken summary tags

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-1
- Added support for both win32 and win64 targets
- Fixed rpmlint issues
- Fixed permissions of the scripts (775 -> 755)
- Fixed description of the various subpackages
- Make the various macros compliant with the new packaging guidelines:
  https://fedorahosted.org/fpc/ticket/71
- Suppress arch-independent-package-contains-binary-or-object rpmlint
  errors for static libraries
- Improved the mingw_configure, mingw_make, mingw_make_install,
  mingw_cmake and mingw_cmake_kde4 RPM macros so packagers don't need
  to use quotes anymore when using arguments. Thanks to Kalev Lember
  for the initial proof of concept
- Dropped the -mms-bitfields argument from the default CFLAGS as
  it is enabled by default as of gcc 4.7
- Replaced the CMake defines QT_HEADERS_DIR and QT_LIBRARY_DIR
  with QT_BINARY_DIR which is a more proper method to make CMake
  aware of the location of Qt. Thx to Dominik Schmidt for the hint
- Make sure CMake can detect the qmake-qt4 binary in /usr/$target/bin
- Make sure CMake can also detect the (native) Qt tools
  qdbuscpp2xml and qdbusxml2cpp
- Added new RPM macros mingw_cmake_kde4, mingw32_cmake_kde4 and mingw64_cmake_kde4
- Added three new environment variables which can be set to
  influence the behaviour of the cmake macros:
  MINGW_CMAKE_ARGS, MINGW32_CMAKE_ARGS and MINGW64_CMAKE_ARGS
- Dropped the mingw32-qmake-qt4 and mingw64-qmake-qt4 wrapper scripts
  as they're now provided by the mingw{32,64}-qt-qmake packages
- Added a new RPM macro: %%{?mingw_package_header}
  Packagers can use this macro instead of the original boilerplate
  code which is needed for all mingw packages
- Made argument passing using the backwards compatibility macro %%{_mingw32_cmake} work
- Fixed an issue in the mingw_cmake macro where it could point to
  a non-existant CMakeLists.txt file
- Fixed a bug in the find-requires script which causes all packages to depend
  on both the mingw32 and the mingw64 toolchains
- Split out the RPM macros which require both the mingw{32,64}-filesystem
  packages in a new file and put it in the mingw-filesystem-base package
- Generate seperate debuginfo packages for mingw32 and mingw64
- Set the minimum version of R: mingw{32,64}-filesystem to 70
- Use the correct FSF-address in some scripts
- Thanks to all the contributors: Erik van Pienbroek, Kalev Lember, Levente
  Farkas, Marc-Andre Lureau.

* Thu Feb 23 2012 Kalev Lember <kalevlember@gmail.com> - 69-15
- Rename the source package to mingw-filesystem (#673784)

* Sun Feb  5 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-14
- Use a more complete list of Win32 default dlls based on the
  dlls exported by wine (thanks to Levente Farkas). RHBZ #787486

* Tue Jan 31 2012 Kalev Lember <kalevlember@gmail.com> - 69-13
- Remove the mingw32-pkg-config wrapper as well, now that we have separate
  mingw32-pkg-config package

* Tue Jan 31 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-12
- Don't provide the wrapper i686-pc-mingw32-pkg-config anymore as we now
  have a mingw32-pkg-config package

* Tue Jan 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-11
- Set Boost_COMPILER to -gcc47 in cmake toolchain file

* Tue Nov 22 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-10
- Fixed a small regression introduced by the previous release which caused an
  FTBFS for mingw32-matahari as indicated on the fedora-mingw mailing list

* Wed Nov 16 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-9
- Added various definitions to the CMake toolchain file (RHBZ #753906)

* Tue Aug 02 2011 Kalev Lember <kalevlember@gmail.com> - 69-8
- Added avicap32.dll and psapi.dll to the list of Win32 default DLLs
  (thanks to Farkas Levente)

* Wed Jul 13 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-7
- Added glu32.dll and wsock32.dll to the list of Win32 default dll's

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-6
- Use a more complete list of Win32 default dll's

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 69-5
- Fixed dep gen with upper case dll names

* Fri Jul  1 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-4
- The %%{_mingw32_qmake_qt4} macro pointed to an invalid mkspecs name. Fixed

* Tue Jun 28 2011 Kalev Lember <kalev@smartlink.ee> - 69-3
- Set Boost_COMPILER to -gcc46 in cmake toolchain file

* Sun May 29 2011 Kalev Lember <kalev@smartlink.ee> - 69-2
- Make sure the -debuginfo subpackages are mingw32- prefixed
  even if the base package is mingw-

* Tue May 24 2011 Kalev Lember <kalev@smartlink.ee> - 69-1
- Adjusted PKG_CONFIG_LIBDIR to also search in _mingw32_datadir/pkgconfig/
- Own the sbin/ directory
- Fixed the -n option with _mingw32_debug_package macro

* Mon May 23 2011 Kalev Lember <kalev@smartlink.ee> - 68-3
- Own etc/, share/pkgconfig/, share/xml/ directories

* Sat May 21 2011 Kalev Lember <kalev@smartlink.ee> - 68-2
- Own the _mingw32_datadir/cmake/ directory

* Fri May 20 2011 Kalev Lember <kalev@smartlink.ee> - 68-1
- Support RPM 4.9 new "fileattr" dep extraction system
- Cleaned up the spec file from cruft not needed with latest rpm
- Generate versionless mingw32-filesystem Requires

* Sat May 14 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 67-1
- Don't unset PKG_CONFIG_PATH in the wrapper scripts
  mingw32-pkg-config and i686-pc-mingw32-pkg-config (BZ #688171)

* Sun May 01 2011 Kalev Lember <kalev@smartlink.ee> - 66-1
- Override boost library suffix in cmake toolchain file

* Thu Mar 17 2011 Kalev Lember <kalev@smartlink.ee> - 65-1
- Don't error out trying to set illegal LD.BFD variable name

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 64-2
- Own the directory %%{_mingw32_datadir}/themes

* Sun Nov 14 2010 Ivan Romanov <drizt@land.ru> - 64-1
- Removed -win32 option for mingw32-qmake-qt4 (is obsoletes since qt version 4.7.0)
- Using win32-g++-fedora-cross instead fedora-win32-cross spec file

* Thu Nov 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 63-1
- Set the CMAKE_RC_COMPILER variable in the CMake toolchain file (RHBZ #652435)

* Tue Oct 19 2010 Ivan Romanov <drizt@land.ru> - 62-2
- Added mingw32-qmake-qt4

* Mon Oct 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 62-1
- Provide mingw32(odbc32.dll) for Qt

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 61-1
- Provide mingw32(gdiplus.dll) for gdk-pixbuf

* Thu Sep  9 2010 Richard W.M. Jones <rjones@redhat.com> - 60-1
- Provide virtual mingw32(ws2_32.dll) for libvirt.

* Mon Sep 06 2010 Kalev Lember <kalev@smartlink.ee> - 59-1
- Own /etc/rpmlint/ dir instead of depending on rpmlint package (RHBZ#629791)

* Fri Sep  3 2010 Richard W.M. Jones <rjones@redhat.com> - 58-1
- Remove requires setup and rpm (RHBZ#629791).

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 57-1
- Add provides mingw32(rpcrt4.dll) (RHBZ#594581).

* Mon May 24 2010 Kalev Lember <kalev@smartlink.ee> - 56-2
- Work around cmake's Qt detection in the toolchain file

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org. - 56-1
- Prevented a circular dependency which caused the i686-pc-mingw32-pkg-config
  script to be broken. Thanks to Kalev Lember for spotting this bug

* Tue Sep  1 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 55-1
- The wrapper scripts i686-pc-mingw32-pkg-config, mingw32-pkg-config,
  mingw32-configure, mingw32-make and mingw32-cmake had a bug where
  quoted arguments could get interpreted incorrect.
  Thanks to Michael Ploujnikov for helping out with this issue

* Sat Aug 29 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 54-1
- Added the file /usr/bin/i686-pc-mingw32-pkg-config which is a wrapper script
  which calls pkg-config with the right environment variables set (BZ #513825)

* Sun Aug 23 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 53-1
- Fixed a small rpmlint warning caused by the debuginfo generation macro
  Thanks to Kalev Lember for spotting this

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 52-2
- Updated ChangeLog comment from previous version as the RPM variable
  __debug_install_post needs to be overridden instead of __os_install_post
  for -debuginfo subpackage generation

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 52-1
- Add script to create -debuginfo subpackages
  This script was created by Fridrich Strba
- All mingw32 packages now need to add these lines to their .spec files:
  %%define __debug_install_post %%{_mingw32_debug_install_post}
  %%{_mingw32_debug_package}

* Thu Jun  4 2009 Adam Goode <adam@spicenitz.org> - 51-1
- Add CMake rules

* Tue Apr 21 2009 Richard W.M. Jones <rjones@redhat.com> - 50-4
- Fix dependency problem with + in DLL name (Thomas Sailer).

* Fri Mar 27 2009 Richard W.M. Jones <rjones@redhat.com> - 50-3
- Fix up and test mingw32-pkg-config changes.

* Thu Mar 26 2009 Levente Farkas <lfarkas@lfarkas.org> - 50-1
- Add mingw32-pkg-config.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 49-2
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 49-1
- Added virtual provides for mingw32(cfgmgr32.dll) and mingw32(setupapi.dll).

* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 48-1
- Fix _mingw32_configure.

* Tue Feb 17 2009 Richard W.M. Jones <rjones@redhat.com> - 47-1
- Rename mingw32-COPYING to COPYING.
- Rename mingw32-macros.mingw32 to macros.mingw32.
- _mingw32_configure looks for configure in "." and ".." dirs.
- Added _mingw32_description.
- Added mingw32(version.dll) virtual provides (rhbz#485842).

* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 46-1
- Unset PKG_CONFIG_PATH because /usr/lib/rpm/macros sets it (Erik van
  Pienbroek).

* Wed Jan 28 2009 Richard W.M. Jones <rjones@redhat.com> - 45-1
- Use PKG_CONFIG_LIBDIR instead of PKG_CONFIG_PATH so that native pkgconfig
  is never searched.

* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 44-1
- Install rpmlint overrides file to suppress some rpmlint warnings.

* Sat Jan 24 2009 Richard W.M. Jones <rjones@redhat.com> - 43-6
- Don't claim C++ compiler exists if it's not installed, as this
  breaks autoconf and (in particular) libtool.

* Wed Jan 14 2009 Richard W.M. Jones <rjones@redhat.com> - 42-1
- Add pseudo-provides secur32.dll

* Wed Dec 17 2008 Levente Farkas <lfarkas@lfarkas.org> - 41-1
- Re-add mingw32-make

* Sat Dec  6 2008 Levente Farkas <lfarkas@lfarkas.org> - 40-2
- Rewrite mingw32-scripts to run in the current shell
- (Re-add mingw32-make) - Removed by RWMJ.
- Add mingw32-env to mingw32.sh

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 39-3
- Unify mingw32-filesystem packages from all three branches again, and test.
- Fix mingw32-scripts so it can handle extra parameters correctly.
- Remove mingw32-env & mingw32-make since neither of them actually work.

* Sun Nov 23 2008 Richard Jones <rjones@redhat.com> - 38-1
- Added mingw32(glut32.dll).

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 37-1
- Revert part of the 36-1 patch.  --build option to configure was wrong.

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 36-1
- Greatly improved macros (Levente Farkas).
- Added -mms-bitfields.

* Thu Nov 13 2008 Richard Jones <rjones@redhat.com> - 35-1
- Added mingw32(wldap32.dll) pseudo-provides.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 34-1
- Set --prefix correctly.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 33-1
- Remove mingw32.{sh,csh} which are unused.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 32-1
- Add mingw32-configure script.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 31-1
- Update the spec file with explanation of the 'Provides: mingw32(...)'
  lines for Windows system DLLs.

* Mon Oct  6 2008 Richard Jones <rjones@redhat.com> - 30-1
- Added _mingw32_cxx.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 29-1
- Added _mingw32_as, _mingw32_dlltool, _mingw32_windres.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 27-1
- Begin the grand renaming of mingw -> mingw32.
- Added mingw32(mscoree.dll).

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 25-1
- Add shared aclocal directory.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 24-1
- Remove mingw-defs, since no longer used.
- Add _mingw_infodir.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 23-1
- Add macros for find-provides/requires scripts

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 22-1
- Windows provides OLE32.DLL.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 21-1
- Allow '.' in dll names for find-requires
- Windows provides GDI32.DLL.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 20-1
- On 64 bit install in /usr/lib/rpm always.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 19-1
- 'user32.dll' is provided by Windows.
- Allow '-' in DLL names.
- More accurate detection of DLLs in requires/provides scripts.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 17-1
- Automatically add mingw-filesystem and mingw-runtime requires.
- Add --prefix to _mingw_configure macro.
- Three backslashes required on each continuation line in RPM macros.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 14-1
- Fix path to mingw-find-requires/provides scripts.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 12-1
- Put CFLAGS on a single line to avoid problems in some configure scripts.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 10-1
- Provides certain base Windows DLLs (not literally).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 9-1
- Include RPM dependency generators and definitions.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4-1
- Add _mingw_cc/cflags/etc. and _mingw_configure macros.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3-1
- Add _mingw_host macro.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Add _mingw_sysroot macro.
- Add _mingw_target macro.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Basic filesystem layout.
