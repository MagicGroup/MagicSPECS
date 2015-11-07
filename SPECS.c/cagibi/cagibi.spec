Name:           cagibi
Version:        0.2.0
Release:        4%{?dist}
Summary:        SSDP (UPnP discovery) cache/proxy daemon
Summary(zh_CN.UTF-8): SSDP(UPnP 探索)缓存/代理守护进程
Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        GPLv2+ and LGPLv2+
URL:            http://www.kde.org/
Source0:        ftp://ftp.kde.org/pub/kde/stable/cagibi/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  qt4-devel
BuildRequires:  cmake

%description
Cagibi is a cache/proxy daemon for SSDP (the discovery part of UPnP).

%description -l zh_CN.UTF-8
Cagibi 是 SSDP(UPnP 探索)缓存/代理守护进程。


%prep
%setup -q

%build
mkdir build
cd build
%{cmake} ..

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB
%{_bindir}/cagibid
#%{_datadir}/dbus-1/services/org.kde.Cagibi.service
# FIXME: devel pkg ? ---nihui
#%{_libdir}/pkgconfig/cagibi.pc
%{_sysconfdir}/cagibid.conf
%{_sysconfdir}/dbus-1/system.d/org.kde.Cagibi.conf
%{_datadir}/dbus-1/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.2.0-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.2.0-3
- 为 Magic 3.0 重建

* Wed Aug 04 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.1.0-2
- Fixed changelog entry
- COPYING.LIB in docs

* Wed Jul 28 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.1.0-1
- Initial package
