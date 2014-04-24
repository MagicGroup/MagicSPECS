%define rversion %{kde4_kdelibs_version}
#define svn_number rc1
%define real_name kde-wallpapers

%define kde4_enable_final_bool OFF

Name: kde4-wallpapers
Summary: Wallpapers for KDE
Summary(zh_CN.UTF-8): KDE4 的墙纸
License: GPL v2 or Later
Group: Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL: http://ktorrent.org
Version: %{rversion}
Release: 2%{?dist}
Source0: http://mirror.bjtu.edu.cn/kde/stable/%{rversion}/src/%{real_name}-%{rversion}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82


%description
Wallpapers for KDE

%description -l zh_CN.UTF-8
KDE4 的墙纸

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
#%doc COPYING
#%{kde4_bindir}/*
#%{kde4_libdir}/*.so*
#%{kde4_plugindir}/*
#%{kde4_iconsdir}/hicolor/*
#%{kde4_xdgappsdir}/*.desktop
#%{kde4_appsdir}/*
#%{kde4_kcfgdir}/*.kcfg
#%{kde4_servicesdir}/*
#%{kde4_servicetypesdir}/*
#%{kde4_configdir}/*
#%{kde4_htmldir}/en/*
%{kde4_datadir}/wallpapers/*

%if 0
%files devel
%defattr(-,root,root,-)
%{kde4_includedir}/*
%{kde4_libdir}/*.so
%endif

%changelog
* Thu Apr 24 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
