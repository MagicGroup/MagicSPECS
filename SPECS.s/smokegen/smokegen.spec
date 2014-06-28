Name: smokegen
Version: 4.13.2
Release: 1%{?dist}
Summary: Smoke Generator

License: LGPLv2 and GPLv2+
URL: https://projects.kde.org/projects/kde/kdebindings/smoke 
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: ftp://ftp.kde.org/pub/kde/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## upstreamable patches

BuildRequires: cmake
BuildRequires: pkgconfig(QtCore) pkgconfig(QtXml) 

Conflicts: kdebindings < 4.7.0

%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
This package includes Smoke Generator.

%package devel
Summary: Development files for Smoke Generator
Conflicts: kdebindings-devel < 4.7.0
Requires: qt4-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LIB
%doc README
%{_libdir}/lib*.so.*

%files devel
%{_bindir}/*
%{_libdir}/lib*.so
%{_libdir}/smokegen/
%{_includedir}/smoke.h
%{_includedir}/smokegen/
%{_datadir}/smoke/
%{_datadir}/smokegen/


%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Mon Mar 05 2012 Liu Di <liudidi@gmail.com> - 4.8.0-3
- 为 Magic 3.0 重建

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for c++ ABI breakage

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.97-1
- 4.7.97

* Thu Dec 22 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95
- drop upstreamed patch

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Thu Nov 24 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Thu Sep 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-3
- %%doc: COPYING COPYING.LIB
- drop Obsoletes: kdebindings (move to smokekde)
- drop deprecated tags from .spec
- drop kde macros

* Fri Sep 16 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- BR: qt4-devel

* Tue Sep 06 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Tue Aug 02 2011 Than Ngo <than@redhat.com> - 4.7.0-2
- patch smoke generator invalid reads found by valgrind

* Tue Jul 26 2011 Than Ngo <than@redhat.com> - 4.7.0-1
- 4.7.0

* Fri Jul 22 2011 Than Ngo <than@redhat.com> - 4.6.95-1
- 4.7 rc1

* Wed Jul 06 2011 Than Ngo <than@redhat.com> - 4.6.90-1
- first Fedora RPM
