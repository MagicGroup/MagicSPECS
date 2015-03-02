
Name:           plasma-mobile
Version:        0.4
Release:        3%{?dist}
Summary:        A Plasma Active mobile workspace

License:        GPLv2+
URL:            http://plasma-active.org/
Source0:        http://download.kde.org/stable/active/3.0/src/%{name}-%{version}.tar.xz
# git archive --prefix=plasma-mobile-0.3/ master | xz > plasma-mobile-0.3-%{snap}.tar.xz
#Source0:        plasma-mobile-0.3-%{snap}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  kde4-kactivities-devel
BuildRequires:  kdepimlibs4-devel
BuildRequires:  kdebase4-workspace-devel
BuildRequires:  pkgconfig(akonadi)
BuildRequires:  pkgconfig(polkit-qt-1) 

Requires:       kde4-filesystem
# temporary require artwork until we have proper active kde-settings
#Requires:       kde-artwork-active

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

Requires:       kdebase4-workspace%{?_kde4_version: >= %{_kde4_version}}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
A touch enabled Plasma Active workspace aiming on different
(not only) mobile devices.

%package devel
Summary: Developer files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.

%package libs
Summary: Runtime libraries for %{name}
%description libs
%{summary}.

%package mouse-cursor-themes
Summary: Plasma Mobile mouse cursor themes
BuildArch: noarch
%description mouse-cursor-themes
%{summary}.

%package wallpapers
Summary: KDE Plasma Active wallpapers
Requires: kde4-filesystem
BuildArch: noarch
%description wallpapers
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

## unpackaged files
rm -rfv %{buildroot}%{_kde4_appsdir}/plasma/services/powermanagementservice.operations


%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
  desktop-file-validate $f ||:
done


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null || :
fi

%files
%doc LICENSE.GPL-2 LICENSE.LGPL-2 LICENSE.LGPL-2.1
%{_kde4_bindir}/active-aboutapp
%{_kde4_bindir}/active-filebrowser
%{_kde4_bindir}/active-settings
%{_kde4_bindir}/active-webbrowser
%{_kde4_bindir}/plasma-device
%{_kde4_bindir}/plasma-widgetstrip
%{_kde4_libdir}/kde4/imports/org/kde/active/
%exclude %{_kde4_libdir}/kde4/imports/org/kde/dirmodel/
%{_kde4_libdir}/kde4/imports/org/kde/metadatamodels/
%{_kde4_libdir}/kde4/imports/org/kde/plasma/mobilecomponents/
%{_kde4_libdir}/kde4/*.so
%{_kde4_libdir}/libkdeinit4_*.so
%{_kde4_libexecdir}/activedatetimehelper
%{_kde4_datadir}/applications/kde4/active-about.desktop
%{_kde4_datadir}/applications/kde4/active-alarms.desktop
%{_kde4_datadir}/applications/kde4/active-books.desktop
%{_kde4_datadir}/applications/kde4/active-filebrowser.desktop
%{_kde4_datadir}/applications/kde4/active-imageviewer.desktop
%{_kde4_datadir}/applications/kde4/active-settings.desktop
%{_kde4_datadir}/applications/kde4/active-web-browser.desktop
%{_kde4_datadir}/applications/kde4/widget-strip.desktop
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_appsdir}/active-webbrowser/
%{_kde4_appsdir}/desktoptheme/air-mobile/
%{_kde4_appsdir}/desktoptheme/default/icons/*
%{_kde4_appsdir}/desktoptheme/oxygen-mobile/
%{_kde4_appsdir}/plasma/
%{_kde4_appsdir}/plasma-widgetstrip/
%{_kde4_appsdir}/solid/actions/browse-files.desktop
%{_kde4_sharedir}/kde4/services/*
%{_kde4_sharedir}/kde4/servicetypes/*
%{_datadir}/dbus-1/system-services/org.kde.active.clockconfig.service
%{_polkit_qt_policydir}/org.kde.active.clockconfig.policy
%{_sysconfdir}/dbus-1/system.d/org.kde.active.clockconfig.conf

%files devel
%{_kde4_includedir}/*.h
%{_kde4_libdir}/libactiveapp.so
%{_kde4_appsdir}/cmake/modules/FindActiveApp.cmake

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/libactiveapp.so.0*

%files mouse-cursor-themes
%{_kde4_iconsdir}/plasmamobilemouse/

%files wallpapers
%{_kde4_datadir}/wallpapers/HorosGreen/


%changelog
* Mon Mar 02 2015 Liu Di <liudidi@gmail.com> - 0.4-3
- 为 Magic 3.0 重建

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4-1
- plasma-mobile-0.4

* Fri Aug 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3-6.20120810git
- 20120810 git snapshot (master branch)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Radek Novacek <rnovacek@redhat.com> 0.3-4
- Rebuild (nepomuk)

* Wed Mar 07 2012 Radek Novacek <rnovacek@redhat.com> 0.3-3
- Rebuild with 4.8.1
- Add BR: kde-runtime-devel

* Tue Feb 21 2012 Radek Novacek <rnovacek@redhat.com> 0.3-2
- Remove file that conflicts with kde-workspace (powermanagementservice.operations)

* Sat Feb 18 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.3-1
- update to 0.3 (PA 2)
- fix buildreqs
- fix filelist
- add polkit-qt-devel for polkit macros

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.2-3
- requires kde-artwork-active

* Thu Nov 10 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.2-2
- split input method to -libs subpackage
- own mobilecomponents directory
- fix desktop file validation

* Mon Nov 07 2011 Jaroslav Reznik <jreznik@redhat.com> - 0.2-1
- initial try
