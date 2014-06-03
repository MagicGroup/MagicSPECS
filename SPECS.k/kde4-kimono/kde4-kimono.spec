#define svn_number rc1
%define real_name kimono

%define kde4_enable_final_bool OFF

Name: kde4-%{real_name}
Summary: .NET/Mono KDE bindings
Summary(zh_CN.UTF-8): .NET/Mono 的 KDE 绑定
License: GPL v2 or Later
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://www.kde.org
Version: 4.13.1
Release: 1%{?dist}
Source0: http://download.kde.org/stable/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake >= 2.6.2
BuildRequires: gettext
BuildRequires: libkdelibs4-devel >= 4.0.82

BuildRequires: pkgconfig(akonadi)
BuildRequires: pkgconfig(mono)
BuildRequires: pkgconfig(monodoc)
BuildRequires: qyoto-devel >= %{version}
BuildRequires: kde4-smokekde-devel >= %{version}

%{?_kde4_version:Requires: qyoto%{?_isa} >= %{_kde4_version}}
%{?_kde4_version:Requires: kde4-smokekde%{?_isa} >= %{_kde4_version}}

%{?mono_arches:ExclusiveArch: %{mono_arches}}

%description
.NET/Mono KDE bindings.

%description -l zh_CN.UTF-8
.NET/Mono 的 KDE 绑定。

%prep
%setup -q -n %{real_name}-%{version}

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
%{kde4_plugindir}/*
%{kde4_libdir}/*.so*
%{_prefix}/lib/mono/*
%{kde4_appsdir}/*
%{kde4_servicesdir}/*

%changelog
* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Sun Apr 27 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Tue Aug 11 2009 Ni Hui <shuizhuyuanluo@126.com> - 3.2.3-1mgc
- 更新至 3.2.3
- 拆出开发包
- 己丑  六月廿一
