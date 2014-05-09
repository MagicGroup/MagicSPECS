# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_with bootstrap
# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_without gui
# Set to RC version if building RC, else %{nil}
%define rcver -rc4

%define rpm_macros_dir %{_sysconfdir}/rpm
%if 0%{?fedora} > 18
%define rpm_macros_dir %{_rpmconfigdir}/macros.d
%endif

Name:           cmake
Version:        3.0.0
Release:        0.5.rc1%{?dist}
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
Source0:        http://www.cmake.org/files/v3.8/cmake-%{version}%{?rcver}.tar.gz
Source1:        cmake-init.el
Source2:        macros.cmake

# Patch to find DCMTK in Fedora (bug #720140)
Patch0:         cmake-dcmtk.patch
# Patch to fix RindRuby vendor settings
# http://public.kitware.com/Bug/view.php?id=12965
# https://bugzilla.redhat.com/show_bug.cgi?id=822796
# Patch to use ninja-build instead of ninja (renamed in Fedora)
# https://bugzilla.redhat.com/show_bug.cgi?id=886184
Patch1:         cmake-ninja.patch
Patch2:         cmake-findruby.patch
# Patch to fix FindPostgreSQL
# https://bugzilla.redhat.com/show_bug.cgi?id=828467
# http://public.kitware.com/Bug/view.php?id=13378
Patch3:         cmake-FindPostgreSQL.patch
# Fix issue with finding consistent python versions
# http://public.kitware.com/Bug/view.php?id=13794
# https://bugzilla.redhat.com/show_bug.cgi?id=876118
Patch4:         cmake-FindPythonLibs.patch
# Add FindLua52.cmake
Patch5:         cmake-2.8.11-rc4-lua-5.2.patch
# Add -fno-strict-aliasing when compiling cm_sha2.c
# http://www.cmake.org/Bug/view.php?id=14314
Patch6:         cmake-strict_aliasing.patch
# Patch away .png extension in icon name in desktop file.
# http://www.cmake.org/Bug/view.php?id=14315
Patch7:         cmake-desktop_icon.patch
# Remove automatic Qt module dep adding
# http://public.kitware.com/Bug/view.php?id=14750
Patch8:         cmake-qtdeps.patch
# Additiona python fixes from upstream
Patch9:         cmake-FindPythonLibs2.patch
# Fix FindwxWiGroup(zh_CN.UTF-8):ets when cross-compiling for Windows
# https://bugzilla.redhat.com/show_bug.cgi?id=1081207
# http://public.kitware.com/Bug/view.php?id=11296
Patch10:         cmake-FindwxWidgets.patch

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# Setup copyright docs for main package
mkdir _doc
find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f _doc/${fname}_${dname}
done

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
mkdir build
pushd build
../bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
             --docdir=/share/doc/%{name} --mandir=/share/man \
             --%{?with_bootstrap:no-}system-libs \
             --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
             %{?qt_gui}
make VERBOSE=1 %{?_smp_mflags}


%install
pushd build
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
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
mkdir -p %{buildroot}%{_libdir}/%{name}

%if %{with gui}
# Desktop file
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/CMake.desktop
%endif
magic_rpm_clean.sh

%if 0%{?with_test}
%check
unset DISPLAY
pushd build
#ModuleNotices fails for some unknown reason, and we don't care
#CMake.HTML currently requires internet access
#CTestTestUpload requires internet access
bin/ctest -V -E ModuleNotices -E CMake.HTML -E CTestTestUpload %{?_smp_mflags}
popd
%endif

%if %{with gui}
%post gui
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun gui
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
%endif

%files
%doc Copyright.txt _doc/*
%{rpm_macros_dir}/macros.cmake
%if %{with gui}
%exclude %{_docdir}/%{name}/cmake-gui.*
%endif
%{_bindir}/ccmake
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/aclocal/cmake.m4
%{_datadir}/bash-completion/
%{_datadir}/%{name}/
%{_emacs_sitelispdir}/%{name}
%{_emacs_sitestartdir}/%{name}-init.el
%{_libdir}/%{name}/

%files doc
%{_docdir}/cmake/*

%if %{with gui}
%files gui
%{_bindir}/cmake-gui
%{_datadir}/applications/CMake.desktop
%{_datadir}/mime/packages/cmakecache.xml
%{_datadir}/pixmaps/CMakeSetup32.png
%endif

%changelog
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


