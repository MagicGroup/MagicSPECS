Name:    kde4-kactivities
%define real_name kactivities
Summary: API for using and interacting with Activities 
Version: %{kde4_kdelibs_version}
Release: 2%{?dist}

License: GPLv2+ and LGPLv2+
URL:     https://projects.kde.org/projects/kde/kdelibs/kactivities
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: ftp://ftp.kde.org/pub/kde/%{stable}/%{version}/src/%{real_name}-%{version}.tar.xz

BuildRequires: kdelibs4-devel >= %{version}

Requires: kdelibs4%{?_isa}%{?_kde4_version: >= %{_kde4_version}}

# libkactivities moved from kdelibs, but turns out there's no actual conflicts
# kactivitymanagerd moved here from kde-runtime 
Conflicts: kdebase-runtime < 4.7.3-10

Obsoletes: libkactivities < 6.1-100
Provides:  libkactivities = 6.1-100

%description
API for using and interacting with Activities as a consumer, 
application adding information to them or as an activity manager.

%package devel
Summary: Developer files for %{name}
Obsoletes: libkactivities-devel < 6.1-100
Provides:  libkactivities-devel = 6.1-100
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.


%prep
%setup -q -n %{real_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kde4_bindir}/kactivitymanagerd
%{_kde4_libdir}/libkactivities.so.6*
%{_kde4_libdir}/kde4/activitymanager_plugin_globalshortcuts.so
%{_kde4_libdir}/kde4/activitymanager_plugin_slc.so
%{_kde4_libdir}/kde4/activitymanager_plugin_sqlite.so
%{_kde4_libdir}/kde4/activitymanager_uihandler_declarative.so
%{_kde4_libdir}/kde4/activitymanager_uihandler_kdialog.so
%{_kde4_libdir}/kde4/kactivitymanagerd_fileitem_linking_plugin.so
%{_kde4_libdir}/kde4/kio_activities.so
%{_kde4_datadir}/kde4/services/activities.protocol
%{_kde4_datadir}/kde4/services/activitymanager-plugin-globalshortcuts.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-slc.desktop
%{_kde4_datadir}/kde4/services/activitymanager-plugin-sqlite.desktop
%{_kde4_datadir}/kde4/services/kactivitymanagerd_fileitem_linking_plugin.desktop
%{_kde4_datadir}/kde4/services/kactivitymanagerd.desktop
%{_kde4_datadir}/kde4/servicetypes/activitymanager-plugin.desktop
%{_kde4_datadir}/ontology/kde/
%dir %{_kde4_appsdir}/plasma/packages/
%{_kde4_appsdir}/plasma/packages/org.kde.ActivityManager.UiHandler/

%files devel
%{_kde4_libdir}/libkactivities.so
%{_kde4_libdir}/cmake/KActivities/
%{_kde4_libdir}/pkgconfig/libkactivities.pc
%{_kde4_includedir}/KDE/KActivities/
%{_kde4_includedir}/kactivities/


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.9.3-2
- 为 Magic 3.0 重建

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Fri Jun 08 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-2
- respin

* Fri May 25 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Radek Novacek <rnovacek@redhat.com> 4.8.1-1
- 4.8.1

* Fri Jan 20 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org>  4.7.80-1
- libkactivities -> kactivities rename

* Fri Nov 04 2011 Rex Dieter <rdieter@fedoraproject.org>  6.1-2
- License: GPLv2+ and LGPLv2+

* Tue Oct 25 2011 Rex Dieter <rdieter@fedoraproject.org>  6.1-1
- first try

