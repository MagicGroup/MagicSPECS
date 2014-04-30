%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name zeroconf-ioslave

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: A framework for searching and managing metadata
Summary(zh_CN.UTF-8): 查找和管理元数据的框架
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Version: %{rversion}
Release: 6%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: kde4-kfilemetadata-devel

BuildRequires: pkgconfig(akonadi) >= 1.11.80
BuildRequires: pkgconfig(QJson)
# for %%{_polkit_qt_policydir} macro
BuildRequires: polkit-qt-devel
BuildRequires: xapian-core-devel

%description
KCharSelect is a tool to select special characters from all installed
fonts and copy them into the clipboard.

%description -l zh_CN.UTF-8
这个程序可以从所有安装的字体中选择特殊字符并复制它们到剪贴板。

%prep
%setup -q -n %{real_name}-%{rversion}

%build
mkdir build
cd build
%cmake_kde4 ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C build

magic_rpm_clean.sh

%clean_kde4_desktop_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LIB
%defattr(-,root,root,-)
%{kde4_plugindir}/*.so
%{kde4_appsdir}/remoteview/zeroconf.desktop
%{kde4_dbus_interfacesdir}/org.kde.kdnssd.xml
%{kde4_servicesdir}/*

%changelog
* Tue Apr 29 2014 Liu Di <liudidi@gmail.com> - 4.13.0-6
- 为 Magic 3.0 重建

* Tue Apr 29 2014 Liu Di <liudidi@gmail.com> - 4.13.0-5
- 为 Magic 3.0 重建

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-4
- 为 Magic 3.0 重建

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-3
- 为 Magic 3.0 重建

* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 4.13.0-1
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
