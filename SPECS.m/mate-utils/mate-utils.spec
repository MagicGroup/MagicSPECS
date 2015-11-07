Name:           mate-utils
Version: 1.11.0
Release: 2%{?dist}
Summary:        MATE utility programs
Summary(zh_CN.UTF-8): MATE 工具程序

License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://pub.mate-desktop.org/releases/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  e2fsprogs-devel
BuildRequires:  hardlink
BuildRequires:  libcanberra-devel
BuildRequires:  libgtop2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXmu-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-panel-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  popt-devel
BuildRequires:  usermode
BuildRequires:  yelp-tools

Requires: mate-dictionary = %{version}-%{release}
Requires: mate-screenshot = %{version}-%{release}
Requires: mate-search-tool = %{version}-%{release}
Requires: mate-system-log = %{version}-%{release}
Requires: mate-disk-usage-analyzer = %{version}-%{release}

%description
The mate-utils package contains a set of small "desk accessory" utility
applications for MATE, such as a dictionary, a disk usage analyzer,
a screen-shot tool and others.

%package common
Summary: Common files for %{name}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for mate-utils
# short-lived mate-dictionary-devel subpkg
Obsoletes: mate-dictionary-devel < 1.6.0-8
#Provides:  mate-dictionary-devel = %{version}-%{release}
Requires:  mate-dictionary%{?_isa} = %{version}-%{release}
%description devel
The mate-utils-devel package contains header files and other resources
needed to develop programs using the libraries contained in mate-utils.

%package -n mate-system-log
Summary: A log file viewer for the MATE desktop
Requires: %{name}-common = %{version}-%{release}
Requires: usermode
# rhbz (#1016935)
Requires: mate-desktop-libs
%description -n mate-system-log
An application that lets you view various system log files.

%package -n mate-screenshot
Summary: A utility to take a screen-shot of the desktop
Requires: %{name}-common = %{version}-%{release}
%description -n mate-screenshot
An application that let you take a screen-shot of your desktop.

%package -n mate-dictionary
Summary: A dictionary for MATE Desktop
Requires: %{name}-common = %{version}-%{release}
%description -n mate-dictionary
The mate-dictionary package contains a dictionary application for MATE Desktop.

%package -n mate-search-tool
Summary: A file searching tool for MATE Desktop
Requires: %{name}-common = %{version}-%{release}
Requires: mate-desktop-libs
%description -n mate-search-tool
An application to search for files on your computer.

%package -n mate-disk-usage-analyzer
Summary: A disk usage analyzing tool for MATE Desktop
Requires: %{name}-common = %{version}-%{release}
%description -n mate-disk-usage-analyzer
An application to help analyze disk usage.

%prep
%setup -q

%build
%configure \
    --disable-static            \
    --disable-schemas-compile   \
    --enable-gdict-applet       \
    --enable-gtk-doc-html       \
    --enable-ipv6=yes           \
    --enable-maintainer-flags=no  \
    --with-gtk=2.0              \
    --with-x

make %{?_smp_mflags} V=1

%install
%{make_install}

# make mate-system-log use consolehelper until it starts using polkit
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cat <<EOF >%{buildroot}%{_sysconfdir}/pam.d/mate-system-log
#%%PAM-1.0
auth      include      config-util
account      include      config-util
session      include      config-util
EOF

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat <<EOF >%{buildroot}%{_sysconfdir}/security/console.apps/mate-system-log
USER=root
PROGRAM=/usr/sbin/mate-system-log
SESSION=true
FALLBACK=true
EOF

mkdir -p  %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/mate-system-log %{buildroot}%{_sbindir}
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/mate-system-log

rm -fv %{buildroot}%{_libdir}/*.la
rm -fv %{buildroot}%{_datadir}/MateConf/gsettings/*.convert

desktop-file-install                          \
  --delete-original                           \
  --dir %{buildroot}%{_datadir}/applications  \
%{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome --all-name
%find_lang mate-disk-usage-analyzer --with-gnome --all-name
%find_lang mate-dictionary --with-gnome --all-name
%find_lang mate-search-tool --with-gnome --all-name
%find_lang mate-system-log --with-gnome --all-name


%postun -n mate-system-log
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n mate-system-log
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%postun -n mate-screenshot
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n mate-screenshot
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%post -n mate-dictionary -p /sbin/ldconfig

%postun -n mate-dictionary
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n mate-dictionary
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%postun -n mate-search-tool
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n mate-search-tool
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%post -n mate-disk-usage-analyzer
/bin/touch --no-create %{_datadir}/icons/mate &> /dev/null || :

%postun -n mate-disk-usage-analyzer
if [ $1 -eq 0 ] ; then
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &> /dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans -n mate-disk-usage-analyzer
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/mate &> /dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
# empty

%files common -f %{name}.lang
%doc COPYING COPYING.libs
%doc NEWS README

%files devel
%{_libdir}/libmatedict.so
%{_libdir}/pkgconfig/mate-dict.pc
%{_includedir}/mate-dict/
%{_datadir}/gtk-doc/html/mate-dict/

%files -n mate-system-log -f mate-system-log.lang
%{_bindir}/mate-system-log
%{_sbindir}/mate-system-log
%{_sysconfdir}/security/console.apps/mate-system-log
%{_sysconfdir}/pam.d/mate-system-log
%{_datadir}/mate-utils/
%{_datadir}/glib-2.0/schemas/org.mate.system-log.gschema.xml
%{_datadir}/applications/mate-system-log.desktop
%{_mandir}/man1/mate-system-log.1.*

%files -n mate-screenshot
%{_bindir}/mate-screenshot
%{_bindir}/mate-panel-screenshot
%{_datadir}/applications/mate-screenshot.desktop
%{_datadir}/mate-screenshot
%{_mandir}/man1/mate-screenshot.1.*
%{_mandir}/man1/mate-panel-screenshot.1.gz
%{_datadir}/glib-2.0/schemas/org.mate.screenshot.gschema.xml

%files -n mate-dictionary -f mate-dictionary.lang
%doc mate-dictionary/AUTHORS
%doc mate-dictionary/README
%{_bindir}/mate-dictionary
%{_datadir}/applications/mate-dictionary.desktop
%{_datadir}/mate-dict/
%{_datadir}/mate-dictionary/
%{_libexecdir}/mate-dictionary-applet
%{_libdir}/libmatedict.so.*
%{_mandir}/man1/mate-dictionary.1.*
%{_datadir}/glib-2.0/schemas/org.mate.dictionary.gschema.xml
%{_datadir}/mate-panel/applets/org.mate.DictionaryApplet.mate-panel-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.DictionaryAppletFactory.service

%files -n mate-search-tool -f mate-search-tool.lang
%{_bindir}/mate-search-tool
%{_datadir}/applications/mate-search-tool.desktop
%{_mandir}/man1/mate-search-tool.1.*
%{_datadir}/glib-2.0/schemas/org.mate.search-tool.gschema.xml
%{_datadir}/pixmaps/mate-search-tool/

%files -n mate-disk-usage-analyzer -f mate-disk-usage-analyzer.lang
%doc baobab/AUTHORS
%doc baobab/README
%{_bindir}/mate-disk-usage-analyzer
%{_datadir}/applications/mate-disk-usage-analyzer.desktop
%{_datadir}/mate-disk-usage-analyzer
%{_mandir}/man1/mate-disk-usage-analyzer.1.*
%{_datadir}/glib-2.0/schemas/org.mate.disk-usage-analyzer.gschema.xml
%{_datadir}/icons/hicolor/*/apps/mate-disk-usage-analyzer.*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.11.0-2
- 更新到 1.11.0

* Mon Aug 11 2014 Liu Di <liudidi@gmail.com> - 1.9.0-2
- 为 Magic 3.0 重建

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- rebuild for libgtop2 soname bump

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- add --disbale-maintainer-flags configure flag

* Tue Feb 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-2
- fix build on ARM
- remove --disable-scrollkeeper configure flag
- add --with-gnome --all-name for find language
- remove usage of hardlink, no need anymore
- fix usage of desktop-file-install
- re-work configure flags
- add BR yelp-tools

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Mon Jan 6 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release
- use modern 'make install' macro
- removed upstreamed patches
- add gtk-doc dir to -devel subpackage
- mate-disk-usage-analyzer icons are renamed, moved to hicolor dir

* Tue Oct 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-10
- add runtime require mate-desktop-libs for mate-system-log, rhbz (#1016935)

* Tue Oct 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-9
- screenshot: do not segfault when taking a window picture with no delay
- fix rhbz (#1022082)
 
* Thu Sep 05 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0-8
- Files and libs duplicated in mate-dictionary and mate-utils (#1003196)
- drop mate-dictionary-devel
- add -common subpkg (for licenses, translations)
- make main empty metapackage, that pulls all subpkgs 
- only mate-system log uses usermode (consolehelper)

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-7
- runtime require mate-desktop-libs for mate-search-tool
- and main package, fix rhbz #988278

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-5
- add upstream patch to fix rhbz #975199

* Tue Jul 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-4
- add mate-dictionary binary to subpackage, rhbz #980434
- add mate-dictionary applet dbus file to subpackage, rhbz #980434
- move baobab docs to mate-disk-usage-analyzer subpackage
- add missing copying files to some subpackages
- move baobab icons to mate-disk-usage-analyzer subpackage
- add baobab icons to main packackes
- add rpm spriptlets for mate-disk-usage-analyzer
- remove mime-types spriptlets,
- because there are not mime-types in desktop files
- remove icon-cache sriptlets from most subpackages,
- only needed for main and mate-disk-usage-analyzer package
- remove glib-compile-schemas from all %%post sections
- remove BR gsettings-desktop-schemas-devel
- remove BR glib2-devel, already called by mate-common
- add -devel subpackage for mate-dictionary
- add mate-search-tool binary to main package
- add /usr/share/mate-dictionary directory to main package

* Sat Jun 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Update gtk-update-icon-cache scriptlet 

* Sat Jun 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Split all the packages up in to sub packages (882184)
- Update source URL
- Remove useless convert files
- Own dirs we're supposed to own

* Sat Apr 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Feb 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-7
- gdict_applet option (don't build by default)
- minor cleanup

* Fri Dec 07 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-6
- revert -5 changes (#884886)

* Thu Nov 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-4
- rebuild for 1.5.0
- drop gdict-applet till upstream fixes it

* Mon Nov 05 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-3
- sort out lang file mess
- link identical immages in help to save space
- fix directory ownership of help files
- add build requires mate-conf-devel
- add build requires desktop-file-utils

* Sun Nov 04 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-2
- add build requires popt-devel

* Tue Oct 23 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Initial build

