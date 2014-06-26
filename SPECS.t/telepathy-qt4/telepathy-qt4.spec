
%if 0%{?fedora} > 16 || 0%{?rhel} >= 7
%define farstream 1
%endif

Name:    telepathy-qt4
Version: 0.9.3
Release: 6%{?dist}
Summary: High-level bindings for Telepathy

License: LGPLv2+
URL:     http://telepathy.freedesktop.org/wiki/Telepathy-Qt4
Source0: http://telepathy.freedesktop.org/releases/telepathy-qt/telepathy-qt-%{version}.tar.gz

## upstreamable patches
# kinda sorta, help find fedora's compat-telepathy-farstream pkg
Patch50: telepathy-qt-0.9.3-farstream_compat.patch
Patch100: telepathy-qt-Qt4Macros-fix.patch

Provides: telepathy-qt = %{version}-%{release} 
Provides: telepathy-qt%{?_isa} = %{version}-%{release}

BuildRequires: cmake
BuildRequires: dbus-python python2-devel
BuildRequires: doxygen
BuildRequires: pkgconfig(gstreamer-interfaces-0.10) 
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtNetwork) pkgconfig(QtXml)
%if 0%{?farstream}
BuildRequires: pkgconfig(farstream-0.1)
%if 0%{?fedora} > 17
## make sure to get the *right* telepathy-farstream
%define compat_telepathy_farstream 1
BuildRequires: compat-telepathy-farstream-devel
BuildRequires: pkgconfig(telepathy-farstream-0.4)
%else
BuildRequires: pkgconfig(telepathy-farstream)
%endif
## unit tests
%define enable_tests -DENABLE_TESTS:BOOL=ON
BuildRequires: pkgconfig(telepathy-glib) >= 0.19
BuildRequires: pkgconfig(gio-2.0)
%endif

Obsoletes: telepathy-qt4-farsight < 0.9.3
Requires: telepathy-mission-control

%description
Telepathy-qt4 are high level bindings for Telepathy and provides both
the low level 1:1 auto generated API, and a high-level API build
on top of that, in the same library.

%package devel
Summary: Development files for %{name}
Provides: telepathy-qt-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: telepathy-filesystem
%if 0%{?farstream}
Requires: %{name}-farstream%{?_isa} = %{version}-%{release}
Obsoletes: telepathy-qt4-farstream-devel < 0.9.1-2
Provides:  telepathy-qt4-farstream-devel = %{version}-%{release} 
Provides:  telepathy-qt-farstream-devel = %{version}-%{release}
%endif
%if 0%{?compat_telepathy_farstream}
## make sure to get the *right* telepathy-farstream deps
Requires: compat-telepathy-farstream-devel%{?_isa}
%endif
%description devel
%{summary}.

%package farstream
Summary: Farstream %{name} bindings
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  telepathy-qt-farstream = %{version}-%{release}
%description farstream 
%{summary}.



%prep
%setup -q -n telepathy-qt-%{version}

%if 0%{?compat_telepathy_farstream}
# should be safe to apply this unconditionally, but...
%patch50 -p1 -b .farstream_compat
%patch100 -p1 -b .findqt
sed -i.farstream_compat \
  -e 's|telepathy-farstream|telepathy-farstream-0.4|g' \
  TelepathyQt/Farstream/TelepathyQtFarstream.pc.in \
  TelepathyQt/Farstream/TelepathyQtFarstream-uninstalled.pc.in
%endif


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  %{?enable_tests}%{!?enable_tests:-DENABLE_TESTS:BOOL=OFF} \
  %{?farstream:-DENABLE_FARSTREAM:BOOL=ON} \
  %{!?farstream:-DENABLE_FARSTREAM:BOOL=OFF} \
  -DENABLE_FARSIGHT:BOOL=OFF \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform} -k


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS NEWS README ChangeLog
%{_libdir}/libtelepathy-qt4.so.2*

%if 0%{?farstream}
%post farstream -p /sbin/ldconfig
%postun farstream -p /sbin/ldconfig

%files farstream
%{_libdir}/libtelepathy-qt4-farstream.so.2*
%endif

%files devel
%doc HACKING
%dir %{_includedir}/telepathy-qt4/
%{_includedir}/telepathy-qt4/TelepathyQt/
%{_libdir}/libtelepathy-qt4.so
%{_libdir}/pkgconfig/TelepathyQt4.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/TelepathyQt4/
%if 0%{?farstream}
%{_libdir}/libtelepathy-qt4-farstream.so
%{_libdir}/pkgconfig/TelepathyQt4Farstream.pc
%{_libdir}/cmake/TelepathyQt4Farstream/
%endif


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.9.3-6
- 为 Magic 3.0 重建

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-5
- fix build for newer compat-telepathy-farstream

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-4
- rework spec/macro conditionals a bit

* Tue Oct 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-3
- (Build)Requires: compat-telepathy-farstream-devel (f18+)

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-2
- rebuild (farstream)

* Fri Aug 03 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-1.1
- move Obsoletes: -farsight to main pkg

* Mon Jul 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-1
- telepathy-qt-0.9.3

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Tue May 22 2012 Radek Novacek <rnovacek@redhat.com> 0.9.1-4
- add rhel condition

* Thu Apr 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-3
- -farsight subpkg (f16)

* Mon Apr 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-2
- drop -farstream-devel subpkg

* Sat Mar 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- 0.9.1
- -farstream(-devel) subpkgs

* Tue Mar 06 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-3
- drop telepathy-farsight support (awaiting upstream -farstream love)

* Fri Feb 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-2
- Requires: telepathy-mission-control

* Wed Jan 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-1
- telepathy-qt-0.9.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-2
- drop Requires: gnome-keyring

* Sat Nov 19 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.0-1
- 0.8.0

* Mon Nov 07 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.3-1
- 0.7.3
- pkgconfig-style deps

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.2-1
- 0.7.2
- Requires: gnome-keyring

* Fri Jul 15 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.7.1-1
- initial package
