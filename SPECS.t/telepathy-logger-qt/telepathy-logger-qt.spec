Name:    telepathy-logger-qt
Version: 15.04.0
Release: 4%{?dist}
Summary: Telepathy Logging for Qt 5
Summary(zh_CN.UTF-8): Qt5 下的 Telepathy 登录框架

License: LGPLv2+
URL:     https://projects.kde.org/projects/extragear/network/telepathy/%{name}

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{name}/%{versiondir}/src/%{name}-%{version}.tar.xz

BuildRequires: extra-cmake-modules
BuildRequires: bison
BuildRequires: cmake
BuildRequires: dbus-python python2-devel
BuildRequires: flex
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(telepathy-logger-0.2)
BuildRequires: pkgconfig(TelepathyQt5)
BuildRequires: pkgconfig(libxml-2.0)

%description
%{summary}
%description -l zh_CN.UTF-8
Qt5 下的 Telepathy 登录框架。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: %{name}%{?_isa} = %{version}-%{release}
# for parent include dir ownership (mostly)
Requires: telepathy-logger-devel%{?_isa}
%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING
%{_libdir}/libtelepathy-logger-qt.so.*

%files devel
%{_includedir}/TelepathyLoggerQt/
%{_libdir}/libtelepathy-logger-qt.so
%{_libdir}/cmake/TelepathyLoggerQt/


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 15.04.0-4
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 15.04.0-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.04.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 15.04.0-1
- Update to 15.04.0 (Qt 5 release)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Jan Grulich <jgrulich@redhat.com> - 0.8.0-1
- 0.8.0

* Mon May 20 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.2-1
- 0.6.2 (set version according to KTp)

* Wed Apr 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.1-1
- 0.6.1

* Tue Apr 02 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.0-1
- 0.6.0

* Thu Mar 07 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.5.80-1
- 0.5.80

* Sun Feb 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.5.3-1
- 0.5.3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Jan Grulich <jgrulich@redhat.com> 0.5.2-1
- 0.5.2

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

