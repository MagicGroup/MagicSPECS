%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name kopete

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: Instant messenger
Summary(zh_CN.UTF-8): 即时消息客户端 
License: GPL v2 or Later
Group: User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL: http://www.kde.org
Version: 4.14.3
Release: 2%{?dist}
Source0: http://download.kde.org/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

#修复在 medistreamer 2.11 以上版本的编译问题
Patch0: 0001-Fix-libjingle-compilation-with-mediastreamer-2.11.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: qt4-xmlpatterns-devel >= 4.8.4

%description
Instant messenger.

%description -l zh_CN.UTF-8
即时消息客户端。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Contains the development files.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q -n %{real_name}-%{rversion}
%patch0 -p1

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
%{kde4_libdir}/*.so*
%{kde4_plugindir}/*
%{kde4_iconsdir}/hicolor/*
%{kde4_xdgappsdir}/*.desktop
%{kde4_appsdir}/*
%{kde4_kcfgdir}/*.kcfg
%{kde4_servicesdir}/*
%{kde4_servicetypesdir}/*
%{kde4_configdir}/*
%{kde4_htmldir}/en/*
#plugin for mozilla
%{kde4_libdir}/mozilla/plugins/skypebuttons.so

%{kde4_dbus_interfacesdir}/*
%{kde4_iconsdir}/oxygen/*
%{kde4_datadir}/sounds/*.ogg

%files devel
%defattr(-,root,root,-)
%{kde4_includedir}/*
%{kde4_libdir}/*.so

%changelog
* Fri Apr 17 2015 Liu Di <liudidi@gmail.com> - 4.14.3-2
- 为 Magic 3.0 重建

* Wed Dec 31 2014 Liu Di <liudidi@gmail.com> - 4.14.3-1
- 更新到 4.14.3

* Mon Nov 03 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Tue Apr 29 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
