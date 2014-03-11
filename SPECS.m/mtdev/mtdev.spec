%global tarball mtdev
%global gitdate 20110105

Name:           mtdev
Version:        1.1.0
Release:        4.%{?gitdate}%{?dist}
Summary:        Multitouch Protocol Translation Library

Group:          System Environment/Libraries
License:        MIT
URL:            http://bitmath.org/code/mtdev/

# upstream doesn't have tarballs
Source0:        %{tarball}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh
Source2:        commitid
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf automake libtool
BuildRequires:  xorg-x11-util-macros >= 1.5.0-1

%description
%{name} is a stand-alone library which transforms all variants of kernel MT
events to the slotted type B protocol. The events put into mtdev may be from
any MT device, specifically type A without contact tracking, type A with
contact tracking, or type B with contact tracking.

%package devel
Summary:        Multitouch Protocol Translation Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Multitouch protocol translation library development package.

%prep
%setup -q -n %{tarball}-%{gitdate}

%build
autoreconf -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README CREDITS
%{_libdir}/libmtdev.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/mtdev.h
%{_includedir}/mtdev-plumbing.h
%{_includedir}/mtdev-mapping.h
%{_libdir}/libmtdev.so
%{_libdir}/pkgconfig/mtdev.pc
%{_bindir}/mtdev-test

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1.0-4.20110105
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3.20110105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2.20110105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-1.20110105
- Update to release 1.1.0

* Tue Aug 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-1.20100803
- Update to release 1.0.8

* Thu Jul 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-2.20100706
- Require util-macros >= 1.5

* Tue Jul 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-1.20100706
- Initial package
