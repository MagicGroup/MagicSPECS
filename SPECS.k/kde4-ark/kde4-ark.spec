%if 0%{?magic}
%global p7zip 1
%endif
#define svn_number rc1
%define real_name ark

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: Archive manager
Summary(zh_CN.UTF-8): 归档管理器
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.13.2
Release: 2%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
%define rversion %version
Source0: http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: bzip2-devel
BuildRequires: desktop-file-utils
BuildRequires: kdebase4-devel >= %{version}
BuildRequires: pkgconfig(libarchive)
BuildRequires: pkgconfig(liblzma) 
BuildRequires: zlib-devel

Requires: kdebase4-runtime%{?_kde4_version: >= %{_kde4_version}}
# Dependencies for archive plugins.
# could split .desktop like okular to support these via
# TryExec=<foo> instead someday -- Rex
Requires: bzip2
Requires: gzip
#Requires: lha
%if 0%{?p7zip}
Requires: p7zip-plugins
%endif
Requires: unzip

%description
Ark is a program for managing various archive formats.

Archives can be viewed, extracted, created and modified from within Ark.
The program can handle various formats such as tar, gzip, bzip2, zip,
rar and lha (if appropriate command-line programs are installed).

%description -l zh_CN.UTF-8
支持多种格式的归档管理器，包括 tar, gzip, bzip2, zip, rar 和 lha 等，
部分格式需要安装相应的命令行程序。

%prep
%setup -q -n %{real_name}-%{rversion}

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%doc COPYING
%{kde4_bindir}/*
%{kde4_plugindir}/*
%{kde4_libdir}/*.so.*
%{kde4_appsdir}/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
%{kde4_kcfgdir}/*
%{kde4_htmldir}/en/*
%{kde4_mandir}/*
%{kde4_libdir}/*.so
%{kde4_iconsdir}/hicolor/*/apps/ark.*

%changelog
* Thu Jul 10 2014 Liu Di <liudidi@gmail.com> - 4.13.2-2
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu May 22 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
