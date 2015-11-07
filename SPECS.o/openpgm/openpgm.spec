Name:          openpgm
Version:       5.2.122
Release:       6%{?dist}
Summary:       An implementation of the PGM reliable multicast protocol
Summary(zh_CN.UTF-8): PGM 可靠组播协议实现

Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# The license is LGPLv2.1
License:       LGPLv2
URL:           http://openpgm.googlecode.com/
Source0:       http://openpgm.googlecode.com/files/libpgm-%{version}~dfsg.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python


%description
OpenPGM is an open source implementation of the Pragmatic General
Multicast (PGM) specification in RFC 3208.

%description -l zh_CN.UTF-8
PGM 可靠组播协议实现。

%package devel
Summary:       Development files for openpgm
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains OpenPGM related development libraries and header files.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libpgm-%{version}~dfsg/openpgm/pgm

%build
%configure
make %{_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm %{buildroot}%{_libdir}/libpgm.{a,la}
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING LICENSE
%{_libdir}/*.so.*


%files devel
%doc examples/
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/openpgm-5.2.pc


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 5.2.122-6
- 为 Magic 3.0 重建

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 5.2.122-5
- 为 Magic 3.0 重建

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.122-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.122-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.2.122-1
- Update to 5.2.122

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.118-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-3
- Build requires python (no longer available by default in F18+ buildroots)

* Fri Dec 21 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-2
- Renamed the tarball (replaced '%7E' by '~')
- Removed the defattr lines

* Wed Dec 19 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-1
- Change license from LGPLv2.1 to LGPLv2 (867182#c13)

* Tue Dec 18 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.1.118-0
- First Fedora specfile

# vim:set ai ts=4 sw=4 sts=4 et:
