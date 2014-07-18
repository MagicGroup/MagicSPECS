Name:    smokeqt
Version: 4.13.3
Release: 1%{?dist}
Summary: Bindings for Qt libraries

License: LGPLv2+
URL:     https://projects.kde.org/projects/kde/kdebindings/smoke
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: ftp://ftp.kde.org/pub/kde/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(qimageblitz)
# qt4-devel
BuildRequires: pkgconfig(QtGui) pkgconfig(QtScript) pkgconfig(QtXml)
BuildRequires: pkgconfig(QtWebKit)
BuildRequires: qscintilla-devel >= 2.4
BuildRequires: qwt-devel
BuildRequires: smokegen-devel >= %{version}

Conflicts: kdebindings < 4.7.0 

%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}
Requires: smokegen%{?_isa} >= %{version}

%description
This package includes Bindings for Qt libraries.

%package devel
Summary: Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: smokegen-devel 
Conflicts: kdebindings-devel < 4.7.0 
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
%doc AUTHORS COPYING.LIB
%{_libdir}/libsmoke*.so.*

%files devel
%{_libdir}/libsmoke*.so
%{_includedir}/smoke/*
%{_datadir}/smokegen/*
%{_datadir}/smoke/*

%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Wed May 28 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Fri Apr 25 2014 Liu Di <liudidi@gmail.com> - 4.13.0-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.7.97-1
- 4.7.97

* Sat Dec 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-2
- rebuild (qsintilla)

* Thu Dec 22 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Thu Nov 24 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3
- more pkgconfig-style deps

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Thu Sep 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-3
- drop kde-deps
- update URL
- remove deprecated tags from .spec
- %%doc: AUTHORS COPYING.LIB

* Fri Sep 16 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- BR: qt4-webkit-devel

* Tue Sep 06 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Than Ngo <than@redhat.com> - 4.7.0-1
- 4.7.0

* Fri Jul 22 2011 Than Ngo <than@redhat.com> - 4.6.95-1
- 4.7 rc1

* Wed Jul 06 2011 Than Ngo <than@redhat.com> - 4.6.90-1
- first Fedora RPM
