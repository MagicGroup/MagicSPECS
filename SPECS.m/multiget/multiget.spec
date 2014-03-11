%define svn 1
%define svndate 20120118
Summary: Cross platform file downloader
Summary(zh_CN.UTF-8): 跨平台的文件下载工具
Name: multiget
Version: 2.0
Release: 0.2%{?dist}
License: GPL
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
#Source0: multiget-%{version}.src.tar.bz2
Source0: multiget-svn%{svndate}.tar.xz
Source1: multiget.desktop
Source2: multiget_download_servicemenu.desktop
Source3: make_multiget_svn_package.sh
Patch1: multiget-1.2.0-fxt.patch
Patch2: multiget-wxgtk29.patch
Patch3: multiget-gcc44.patch
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: glibc >= 2.2.0

%description
MultiGet is an easy-to-use GUI file downloader for Windows/Linux/BSDs/MacOs.  
It's programmed in C++ and has a GUI based on wxWidgets. 

%description -l zh_CN.UTF-8
MultiGet 是一个易用的图形界面文件下载管理器，可运行在
Windows/Linux/BSD/MacOS 上。它使用 C++ 编程，并拥有
一个基于 wxWidgets 的图形界面。

%prep
%setup -q -n %{name}-svn%{svndate}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
autoreconf -fisv
./configure --prefix=%{_prefix} --disable-shared --enable-monolithic --with-gtk=2 --with-libpng=builtin --with-zlib=builtin --with-expat=builtin --with-libtiff=builtin --with-regex=builtin --with-libjpeg=builtin --enable-unicode
%{__make} %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -D -m 644 icons/mg_32.xpm %{buildroot}%{_datadir}/pixmaps/mg_32.xpm
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/multiget.desktop
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/apps/konqueror/servicemenus/d4x_download_servicemenu.desktop
#fix the wrong doc dir
mv %{buildroot}%{_usr}/doc %{buildroot}%{_datadir}/
#pushd %{buildroot}%{_bindir}
#mv multiget multiget.orig
#cat >> multiget << EOF
#!/bin/bash
#case \$LANG in
#zh_CN.UTF-8|zh_CN.gb18030|zh_CN.GBK|zh_CN.gbk|zh_CN.GB2312|zh_CN.gb2312)
#LC_ALL=zh_CN.GB2312 multiget.orig;;
#*);;
#esac
#EOF
#chmod 755 multiget
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%{_bindir}
%{_datadir}
#%{_usr}
#%exclude %{_usr}/*/debug*
#%exclude %{_usrsrc}

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0-0.2
- 为 Magic 3.0 重建

* Mon Dec 10 2007 kde <athena_star {at} 163 {dot} com> - 1.2.0-2mgc
- standardize the spec file and fix the translation of the spec file
- add a servicemenu for konqueror
- fix the wrong doc dir

* Sun Nov 11 2007 haulm <haulm@126.com> - 1.2.0-1mgc
- update to 1.2.0

* Fri Mar 09 2007 Liu Di <liudidi@gmail.com> - 1.1.4-1mgc
- update to 1.1.4

* Tue Jan 30 2007 Liu Di <liudidi@gmail.com> - 1.1.2-1mgc
- first packages for Magic Linux
