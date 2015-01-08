#define svn_number rc1
%define real_name okular

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: A document viewer
Summary(zh_CN.UTF-8): 文档阅读器
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.14.3
Release: 1%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz
Patch1:	okular-4.9.2-patch1.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

BuildRequires: chmlib-devel
BuildRequires: desktop-file-utils
BuildRequires: djvulibre-devel
BuildRequires: ebook-tools-devel
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kde4-libkipi-devel >= %{version}
BuildRequires: libspectre-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(poppler-qt4)
BuildRequires: pkgconfig(qca2)
BuildRequires: qimageblitz-devel
BuildRequires: plasma-mobile-devel

%description
A document viewer

%description -l zh_CN.UTF-8
文档阅读器。

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。包含 libbtcore 的开发文件。

%prep
%setup -q -n %{real_name}-%{version}
#%patch1 -p1

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
%{kde4_iconsdir}/hicolor/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
#%{kde4_localedir}/*
%{kde4_htmldir}/en/*
%{kde4_kcfgdir}/*
%{kde4_mandir}/man1/okular.1*

%files devel
%defattr(-,root,root,-)
%{kde4_libdir}/*.so
%{kde4_includedir}/*
%{kde4_libdir}/cmake/*

%changelog
* Tue Dec 30 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Wed Oct 22 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
