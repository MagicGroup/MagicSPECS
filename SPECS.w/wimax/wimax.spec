%global gitdate 20110419
%global gitrev 6718941c

Name:       wimax
Summary:    WiMAX Network Service for the Intel 2400m
Version:    1.5.2
Release:    6%{?gitdate:.%{gitdate}git%{gitrev}}%{dist}
Group:      System Environment/Base
License:    BSD
URL:        http://linuxwimax.org/
# To recreate the tarball, do "./make-git-snapshot.sh %{gitrev}"
%if 0%{?gitdate}
Source0:    wimax-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0: http://linuxwimax.org/Download?action=AttachFile&do=get&target=wimax-1.5.1.tar.gz
%endif
# Clean up manpage syntax
Patch1: wimax-1.5.2-noise.patch
# Don't handle dhclient ourselves
Patch2: wimax-1.5.2-iprenew.patch
BuildRequires: wimax-tools-devel >= 1.4.5-2
BuildRequires: zlib-devel
BuildRequires: libeap-devel >= 1:1.0-0.3
BuildRequires: chrpath
ExcludeArch: s390 s390x

%description
User space daemon for the Intel 2400m Wireless WiMAX Link.
This daemon takes care of handling network scan, discovery and
management.

%package libs
Summary:    Libraries for WiMAX network service
Group:      System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Runtime libraries for the WiMAX network service.

%package devel
Summary:    Development files for WiMAX Low Level Tools
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}-%{release}
Requires:   pkgconfig

%description devel
Header files and libraries needed to link to the WiMAX network service.

%prep
%setup -q -n %{name}-%{gitdate}
%patch1 -p1 -b .man-noise
%patch2 -p1 -b .renew

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

find %{buildroot} -name "*.a" -exec rm -f {} \;
find %{buildroot} -name "*.la" -exec rm -f {} \;

chrpath --delete %{buildroot}%{_bindir}/wimaxd

mv %{buildroot}/etc/logrotate.d/wimax.conf %{buildroot}/etc/logrotate.d/wimax

mkdir -p %{buildroot}%{_prefix}/lib/udev
mv %{buildroot}/etc/udev/rules.d %{buildroot}%{_prefix}/lib/udev

magic_rpm_clean.sh

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.txt CHANGELOG LICENSE INSTALL
%config /etc/logrotate.d/wimax
%config /etc/modprobe.d/i2400m.conf
%config /etc/wimax/config.xml
%{_prefix}/lib/udev/rules.d/iwmxsdk.rules
%{_bindir}/wimaxcu
%{_bindir}/wimaxd
%{_bindir}/wimax_monitor
%{_mandir}/man1/*
%{_datadir}/wimax
%{_sharedstatedir}/wimax

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.0*

%files devel
%defattr(-,root,root,-)
%{_includedir}/wimax
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.5.2-6.20110419git6718941c
- 为 Magic 3.0 重建

* Mon Apr 23 2012 Liu Di <liudidi@gmail.com> - 1.5.2-5.20110419git6718941c
- 为 Magic 3.0 重建

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 1.5.2-4.20110419git6718941c
- Rebuild against libnl3-enabled libeap

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3.20110419git6718941c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 19 2011 Bill Nottingham <notting@redhat.com> - 1.5.2-2.20110419git6718941c
- update to upstream tagged 1.5.2
- fix assorted issues from package review
- don't handle dhclient ourselves

* Tue Mar 22 2011 Bill Nottingham <notting@redhat.com> - 1.5.1-1.20110322gitbefcae11
- initial packaging
