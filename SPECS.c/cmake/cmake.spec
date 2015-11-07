# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_with bootstrap
# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_without gui
# Set to RC version if building RC, else %{nil}
#define rcver -rc4

%define rpm_macros_dir %{_rpmconfigdir}/macros.d

Name:           cmake
Version:	3.3.2
Release:        2%{?dist}
Summary:        Cross-platform make system
Summary(zh_CN.UTF-8): 跨平台的 make 系统

Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
# most sources are BSD
# Source/CursesDialog/form/ a bunch is MIT 
# Source/kwsys/MD5.c is zlib 
# some GPL-licensed bison-generated files, these all include an exception granting redistribution under terms of your choice
License:        BSD and MIT and zlib
URL:            http://www.cmake.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://www.cmake.org/files/v%{majorver}/cmake-%{version}%{?rcver}.tar.gz
Source1:        cmake-init.el
Source2:        macros.cmake
# See https://bugzilla.redhat.com/show_bug.cgi?id=1202899
Source3:        cmake.attr
Source4:        cmake.prov

# Patch to find DCMTK in Fedora (bug #720140)
Patch0:         cmake-dcmtk.patch
# Patch to fix RindRuby vendor settings
# http://public.kitware.com/Bug/view.php?id=12965
# https://bugzilla.redhat.com/show_bug.cgi?id=822796
Patch2:         cmake-findruby.patch
# Fix issue with redhat-hardened-ld
# http://www.cmake.org/Bug/view.php?id=15737
# https://bugzilla.redhat.com/show_bug.cgi?id=1260490
Patch3:         cmake.git-97ffbcd8.patch

## upstream patches
# some post v3.3.1 tag commits
Patch624:       0624-FindBoost-Add-support-for-Boost-1.59.patch
Patch640:       0640-FindPkgConfig-remove-variable-dereference.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran
BuildRequires:  ncurses-devel, libX11-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  libarchive-devel
BuildRequires:  zlib-devel
BuildRequires:  emacs
%if %{without bootstrap}
#BuildRequires: xmlrpc-c-devel
%endif
%if %{with gui}
BuildRequires: qt4-devel, desktop-file-utils
%define qt_gui --qt-gui
%endif

Requires:       rpm

Requires: emacs-filesystem >= %{_emacs_version}

# Source/kwsys/MD5.c
# see https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(md5-deutsch)

%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.

%description -l zh_CN.UTF-8
CMake是一个跨平台的安装(编译)工具,可以用简单的语句来描述所有平台的安装(编译过程)。
他能够输出各种各样的makefile或者project文件,能测试编译器所支持的C++特性,类似UNIX
下的automake。只是 CMake 的组态档取名为 CmakeLists.txt。


%package        gui
Summary:        Qt GUI for %{name}
Summary(zh_CN.UTF-8): 用 Qt 写的 %{name} 图形界面
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires:       %{name} = %{version}-%{release}

%description    gui
The %{name}-gui package contains the Qt based GUI for CMake.

%description gui -l zh_CN.UTF-8
用 Qt 写的 %{name} 图形界面。

%package        doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains documentation for CMake.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{name}-%{version}%{?rcver}

# We cannot use backups with patches to Modules as they end up being installed
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch624 -p1
%patch640 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
mkdir build
pushd build
../bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
             --docdir=/share/doc/%{name} --mandir=/share/man \
             --%{?with_bootstrap:no-}system-libs \
             --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
             --sphinx-man \
             %{?qt_gui}
make VERBOSE=1 %{?_smp_mflags}

%install
pushd build
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
[ -n "$(find %{buildroot}/%{_datadir}/%{name}/Modules -name \*.orig)" ] &&
  echo "Found .orig files in %{_datadir}/%{name}/Modules, rebase patches" &&
  exit 1
popd
# Install bash completion symlinks
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
for f in %{buildroot}%{_datadir}/%{name}/completions/*
do
  ln -s ../../%{name}/completions/$(basename $f) %{buildroot}%{_datadir}/bash-completion/completions/
done
# Install emacs cmake mode
mkdir -p %{buildroot}%{_emacs_sitelispdir}/%{name}
install -p -m 0644 Auxiliary/cmake-mode.el %{buildroot}%{_emacs_sitelispdir}/%{name}/
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/%{name}/cmake-mode.el
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 %SOURCE1 %{buildroot}%{_emacs_sitestartdir}/
# RPM macros
install -p -m0644 -D %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.cmake
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" %{buildroot}%{rpm_macros_dir}/macros.cmake
touch -r %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.cmake
%if 0%{?_rpmconfigdir:1}
# RPM auto provides
install -p -m0644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/rpm/fileattrs/cmake.attr
install -p -m0755 -D %{SOURCE4} %{buildroot}%{_prefix}/lib/rpm/cmake.prov
%endif
mkdir -p %{buildroot}%{_libdir}/%{name}
# Install copyright files for main package
cp -p Copyright.txt %{buildroot}/%{_docdir}/%{name}/
find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f %{buildroot}/%{_docdir}/%{name}/${fname}_${dname}
done

%if %{with gui}
# Desktop file
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/CMake.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_datadir}/appdata
cat > %{buildroot}%{_datadir}/appdata/CMake.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Ryan Lerch <rlerch@redhat.com> -->
<!--
EmailAddress: kitware@kitware.com
SentUpstream: 2014-09-17
-->
<application>
  <id type="desktop">CMake.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>CMake GUI</name>
  <summary>Create new CMake projects</summary>
  <description>
    <p>
      CMake is an open source, cross platform build system that can build, test,
      and package software. CMake GUI is a graphical user interface that can
      create and edit CMake projects.
    </p>
  </description>
  <url type="homepage">http://www.cmake.org</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/CMake/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

%endif


%check
unset DISPLAY
pushd build
#CMake.FileDownload, and CTestTestUpload require internet access
bin/ctest -V -E 'CMake.FileDownload|CTestTestUpload' %{?_smp_mflags}
popd


%if %{with gui}
%post gui
update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/mime || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif


%files
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/Copyright.txt*
%{_docdir}/%{name}/COPYING*
%{rpm_macros_dir}/macros.cmake
%if 0%{?_rpmconfigdir:1}
%{_prefix}/lib/rpm/fileattrs/cmake.attr
%{_prefix}/lib/rpm/cmake.prov
%endif
%{_bindir}/ccmake
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/aclocal/cmake.m4
%{_datadir}/bash-completion/
%{_datadir}/%{name}/
%{_mandir}/man1/ccmake.1.gz
%{_mandir}/man1/cmake.1.gz
%{_mandir}/man1/cpack.1.gz
%{_mandir}/man1/ctest.1.gz
%{_mandir}/man7/*.7.gz
%{_emacs_sitelispdir}/%{name}
%{_emacs_sitestartdir}/%{name}-init.el
%{_libdir}/%{name}/

%files doc
%{_docdir}/%{name}/

%if %{with gui}
%files gui
%{_bindir}/cmake-gui
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/CMake.desktop
%{_datadir}/mime/packages/cmakecache.xml
%{_datadir}/icons/hicolor/*/apps/CMakeSetup.png
%{_mandir}/man1/cmake-gui.1.gz
%endif

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 3.3.2-2
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 3.3.2-1
- 更新到 3.3.2

* Thu Aug 14 2014 Liu Di <liudidi@gmail.com> - 3.0.1-0.6.rc1
- 更新到 3.0.1

* Wed Jul 09 2014 Liu Di <liudidi@gmail.com> - 3.0.0-0.6.rc1
- 为 Magic 3.0 重建

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 3.0.0-0.5.rc1
- 为 Magic 3.0 重建

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 3.0.0-0.4.rc1
- 为 Magic 3.0 重建

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 3.0.0-0.3.rc1
- 为 Magic 3.0 重建

* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 3.0.0-0.2.rc1
- 为 Magic 3.0 重建

* Wed Mar 12 2014 Liu Di <liudidi@gmail.com> - 2.8.12.2-2
- 更新到 2.8.12.2

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.8.9-2
- 为 Magic 3.0 重建


