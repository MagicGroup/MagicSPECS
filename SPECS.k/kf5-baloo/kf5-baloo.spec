%define         framework baloo

Name:           kf5-%{framework}
Summary:        A Tier 3 KDE Frameworks 5 module that provides indexing and search functionality
Version:        5.17.0
Release:        1%{?dist}

# libs are LGPL, tools are GPL
# KDE e.V. may determine that future LGPL/GPL versions are accepted
License:        (LGPLv2 or LGPLv3) and (GPLv2 or GPLv3)
URL:            https://projects.kde.org/projects/kde/kdelibs/baloo

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

Source1:        97-kde-baloo-filewatch-inotify.conf

## upstreamable patches
# http://bugzilla.redhat.com/1235026
Patch1: baloo-5.14.0-baloofile_config.patch

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules >= %{version}
BuildRequires:  kf5-kconfig-devel >= %{version}
BuildRequires:  kf5-kcoreaddons-devel >= %{version}
BuildRequires:  kf5-kcrash-devel >= %{version}
BuildRequires:  kf5-kdbusaddons-devel >= %{version}
BuildRequires:  kf5-kfilemetadata-devel >= %{version}
BuildRequires:  kf5-ki18n-devel >= %{version}
BuildRequires:  kf5-kidletime-devel >= %{version}
BuildRequires:  kf5-kio-devel >= %{version}
BuildRequires:  kf5-rpm-macros >= %{version}
BuildRequires:  kf5-solid-devel >= %{version}
BuildRequires:  lmdb-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel


Requires:       kf5-filesystem >= %{version}

Obsoletes:      kf5-baloo-tools < 5.5.95-1
Obsoletes:      baloo < 5
Provides:       baloo = %{version}-%{release}

%description
%{Summary}.

%package        devel
Summary:        Development files for %{name}
# KDE e.V. may determine that future LGPL versions are accepted
License:        LGPLv2 or LGPLv3
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-file%{?_isa} = %{version}-%{release}
Requires:       kf5-kcoreaddons-devel >= %{version}
Requires:       kf5-kfilemetadata-devel >= %{version}
Requires:       qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        file
Summary:        File indexing and search for Baloo
# KDE e.V. may determine that future LGPL versions are accepted
License:        LGPLv2 or LGPLv3
Obsoletes:      %{name} < 5.0.1-2
Obsoletes:      baloo-file < 5.0.1-2
Provides:       baloo-file = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
%description    file
%{summary}.

%package        libs
Summary:        Runtime libraries for %{name}
# KDE e.V. may determine that future LGPL versions are accepted
License:        LGPLv2 or LGPLv3
%description    libs
%{summary}.


%prep
%setup -qn %{framework}-%{version}

%patch1 -p1 -b .baloofile_config


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

install -p -m644 -D %{SOURCE1} %{buildroot}%{_prefix}/lib/sysctl.d/97-kde-baloo-filewatch-inotify.conf

%find_lang kio_baloosearch --with-qt
%find_lang kio_tags --with-qt
%find_lang kio_timeline --with-qt
%find_lang balooctl --with-qt
%find_lang baloosearch --with-qt
%find_lang balooshow --with-qt
%find_lang baloo_file --with-qt
%find_lang baloo_file_extractor --with-qt
%find_lang baloomonitorplugin --with-qt

cat kio_tags.lang kio_baloosearch.lang kio_timeline.lang balooctl.lang baloosearch.lang balooshow.lang baloomonitorplugin.lang \
    > %{name}.lang

cat baloo_file.lang baloo_file_extractor.lang \
    > %{name}-file.lang

%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
fi

%files -f %{name}.lang
%license COPYING
%{_kf5_bindir}/baloosearch
%{_kf5_bindir}/balooshow
%{_kf5_bindir}/balooctl
%{_kf5_plugindir}/kio/baloosearch.so
%{_kf5_plugindir}/kio/tags.so
%{_kf5_plugindir}/kio/timeline.so
%{_kf5_plugindir}/kded/baloosearchmodule.so
%{_kf5_qmldir}/org/kde/baloo
%{_kf5_datadir}/kservices5/baloosearch.protocol
%{_kf5_datadir}/kservices5/tags.protocol
%{_kf5_datadir}/kservices5/timeline.protocol
%{_kf5_datadir}/icons/hicolor/*/apps/baloo.png

%files file -f %{name}-file.lang
%{_prefix}/lib/sysctl.d/97-kde-baloo-filewatch-inotify.conf
%{_kf5_bindir}/baloo_file
%{_kf5_bindir}/baloo_file_extractor
%{_kf5_sysconfdir}/xdg/autostart/baloo_file.desktop

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%license COPYING.LIB
%{_kf5_libdir}/libKF5Baloo.so.*
%{_kf5_libdir}/libKF5BalooEngine.so.*

%files devel
%{_kf5_libdir}/libKF5Baloo.so
%{_kf5_libdir}/cmake/KF5Baloo/
%{_kf5_libdir}/pkgconfig/Baloo.pc
%{_kf5_includedir}/Baloo/
%{_kf5_includedir}/baloo_version.h
%{_kf5_datadir}/dbus-1/interfaces/org.kde.baloo.*.xml


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.16.0-1
- KDE Frameworks 5.16.0

* Thu Oct 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.15.0-1
- KDE Frameworks 5.15.0

* Sat Oct 03 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-2
- index only well-known document-centric dirs by default (#1235026)
- .spec cosmetics
- polish licensing
- -devel: drop xapian dep

* Wed Sep 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.14.0-1
- KDE Frameworks 5.14.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13 (Baloo moved from Plasma 5 to KF5)

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.1-1
- Plasma 5.2.1

* Sun Feb 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-3
- kf5-baloo-file provides baloo-file

* Sat Feb 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-2
- port 97-kde-baloo-filewatch-inotify.conf from Obsoletes'd baloo pkg

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- Plasma 5.2.0

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.95-1
- Plasma 5.1.95 (Plasma 5.2 beta) (baloo 5.5.95 to follow KF5)
- create -libs subpkg

* Wed Jan 07 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.2-3
- Drop -tools subpkg
-  Add icon cache scriptlets
-  Remove deprecated Group: tag
-  Move org.kde.baloo.file.indexer.xml to -file subpkg

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Mon Aug 18 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-2
- Fix coinstallability with updated baloo package

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Tue Jul 22 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-4
- -devel Requires xapian-core-devel

* Tue Jul 22 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-3
- split bin tools to -tools subpackage

* Tue Jul 22 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- -devel Requires kf5-kfilemetadata-devel
- does not obsolete baloo < 5.0.0 (coinstallability)

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-3.20140611git84bc23c
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-2.20140611git46e3ea7
- KF5 Baloo 4.90.0 (git snapshot built from common kdepimlibs/frameworks repo)
