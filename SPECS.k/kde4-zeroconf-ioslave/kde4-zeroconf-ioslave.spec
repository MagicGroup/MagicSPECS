#define svn_number rc1
%define real_name zeroconf-ioslave

%define kde4_enable_final_bool ON

Name: kde4-%{real_name}
Summary: KDE Network Monitor for DNS-SD services (Zeroconf)
Summary(zh_CN.UTF-8): DNS-SD 服务的网络监视器
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Version: 4.14.3
Release: 2%{?dist}
License: LGPL
URL: http://extragear.kde.org/apps/kipi
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz
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
KDE Network Monitor for DNS-SD services (Zeroconf).

%description -l zh_CN.UTF-8
DNS-SD 服务的网络监视器。

%prep
%setup -q -n %{real_name}-%{version}

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
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

* Wed Dec 31 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Fri Oct 31 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Thu Jun 05 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

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
