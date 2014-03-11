%define rversion 0.4.0
%define real_name synaptiks

%define with_xinput2 1
#define kde4_enable_final_bool OFF

Name: kde4-synaptiks
Summary: synaptiks is a touchpad service for KDE 4
Summary(zh_CN.UTF-8): synaptiks 是个 KDE4 触摸板服务
License: BSD
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://synaptiks.lunaryorn.de
Version: %{rversion}
Release: 3%{?dist}
Source0: http://bitbucket.org/lunar/synaptiks/downloads/%{real_name}-%{version}.tar.bz2
Source1: synaptiks.po

Patch1: synaptiks-0.4.0-desktop-zh_CN.patch
Patch2: synaptiks-0.4.0-disable-touchpadmissing-notify.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82
BuildRequires: libkdepimlibs4-devel
BuildRequires: phonon-devel

%if %with_xinput2
BuildRequires: xorg-x11-proto-devel >= 7.5
%endif

%description
This service configures and manages your touchpad.

%description -l zh_CN.UTF-8
本服务可配置和管理您的触摸板。


%prep
%setup -q -n %{real_name}-%{version}

%patch1 -p1 -b .zh_CN
%patch2 -p1 -b .notify

rm -rf doc-translations/*

%build
mkdir build
cd build
%cmake_kde4 \
%if %with_xinput2
    -DWITH_XINPUT2=ON \
%else
    -DWITH_XINPUT2=OFF \
%endif
    ..

make %{?_smp_mflags}

%install
cd build
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{kde4_localedir}/zh_CN/LC_MESSAGES
msgfmt %{SOURCE1} -o %{buildroot}%{kde4_localedir}/zh_CN/LC_MESSAGES/synaptiks.mo

magic_rpm_clean.sh

%clean_kde4_desktop_files
%clean_kde4_notifyrc_files
%adapt_kde4_notifyrc_files

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-,root,root,-)
#%doc COPYING README
%{kde4_plugindir}/*
%{kde4_appsdir}/*
%{kde4_kcfgdir}/*
%{kde4_dbus_interfacesdir}/*
%{kde4_iconsdir}/*
%{kde4_servicesdir}/*
%{kde4_localedir}/*
%doc %lang(en) %{kde4_htmldir}/en/synaptiks

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.0-3
- 为 Magic 3.0 重建

* Wed Apr 21 2010 Ni Hui <shuizhuyuanluo@126.com> - 0.4.0-1mgc
- 首次生成 rpm 包
- 庚寅  三月初八
