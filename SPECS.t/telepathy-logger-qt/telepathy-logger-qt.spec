Name:    telepathy-logger-qt
Version: 0.5.1
Release: 3%{?dist}
Summary: Telepathy Logging for Qt 

License: LGPLv2+
URL:     https://projects.kde.org/projects/extragear/network/telepathy/%{name}
Source0: http://download.kde.org/unstable/kde-telepathy/%{version}/src/%{name}-%{version}.tar.bz2

## upstreamable patches
# pkgconfig Requires.private: +QtGLib 
Patch50: telepathy-logger-qt-0.4.0-pkgconfig_QtGLib.patch

BuildRequires: bison
BuildRequires: cmake
BuildRequires: dbus-python python2-devel
BuildRequires: flex
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(QtGLib-2.0)
BuildRequires: pkgconfig(telepathy-logger-0.2)
BuildRequires: pkgconfig(TelepathyQt4) >= 0.9
BuildRequires: pkgconfig(libxml-2.0)

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# for parent include dir ownership (mostly)
Requires: telepathy-logger-devel%{?_isa}
%description devel
%{summary}.


%prep
%setup -q -n telepathy-logger-qt-%{version}

%patch50 -p1 -b pkgconfig_QtGLib


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING
%{_libdir}/libtelepathy-logger-qt4.so.1*

%files devel
%{_includedir}/telepathy-logger-0.2/TelepathyLoggerQt4/
%{_libdir}/libtelepathy-logger-qt4.so
%{_libdir}/pkgconfig/TelepathyLoggerQt4.pc


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.5.1-3
- 为 Magic 3.0 重建

* Wed Oct 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-2
- rebuild (telepathy-logger)

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.5.1-1
- 0.5.1

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.5.0-1
- 0.5.0

* Sat Jul 28 2012 Jan Grulich <jgrulich@redhat.com> - 0.4.1-2
- Fix libraries in %%files

* Thu Jul 26 2012 Jan Grulich <jgrulich@redhat.com> - 0.4.1-1
- 0.4.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- QtGLib pkgconfig patch

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- first try

