%global _changelog_trimtime %(date +%s -d "1 year ago")

%global with_nautilus 0

%if 0%{?rhel}
%global with_enca 0
%global with_libcue 0
%global with_thunderbird 0
%else
%global with_enca 1
%global with_libcue 1
%global with_thunderbird 1
%endif

Summary:	Desktop-neutral search tool and indexer
Name:		tracker
Version:	0.17.4
Release:	2%{?dist}
License:	GPLv2+
Group:		Applications/System
URL:		http://projects.gnome.org/tracker/
Source0:	http://download.gnome.org/sources/tracker/0.17/%{name}-%{version}.tar.xz

# only autostart in Gnome, see also
# https://bugzilla.redhat.com/show_bug.cgi?id=771601
Patch1:		tracker-0.15-onlyshowin.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=712142
Patch3:		0001-Bump-the-minimum-memory-requirement-to-768M.patch

BuildRequires:	desktop-file-utils
%if 0%{?with_enca}
BuildRequires:	enca-devel
%endif
BuildRequires:	exempi-devel
BuildRequires:	firefox
BuildRequires:	flac-devel
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	giflib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	graphviz
BuildRequires:	gstreamer1-devel
BuildRequires:	gstreamer1-plugins-base-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk3-devel
BuildRequires:	gupnp-dlna-devel
BuildRequires:	intltool
%if 0%{?with_libcue}
BuildRequires:	libcue-devel
%endif
BuildRequires:	libexif-devel
BuildRequires:	libgee-devel
BuildRequires:	libgsf-devel
BuildRequires:	libgxps-devel
BuildRequires:	libicu-devel
BuildRequires:	libiptcdata-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmediaart-devel
BuildRequires:	libosinfo-devel
BuildRequires:	libpng-devel
BuildRequires:	libsecret-devel
BuildRequires:	libtiff-devel
BuildRequires:	libuuid-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
%if 0%{?with_nautilus}
BuildRequires:	nautilus-devel
%endif
BuildRequires:	NetworkManager-glib-devel
BuildRequires:	poppler-glib-devel
BuildRequires:	rest-devel
BuildRequires:	sqlite-devel
BuildRequires:	taglib-devel
%if 0%{?with_thunderbird}
BuildRequires:	thunderbird
%endif
BuildRequires:	totem-pl-parser-devel
BuildRequires:	upower-devel
BuildRequires:	vala-devel

Obsoletes: compat-tracker018 < 0.17.2-2
Obsoletes: tracker-miner-flickr < 0.16.0
Obsoletes: tracker-nautilus-plugin < 0.17.2-2

%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database, search tool and indexer.

It consists of a common object database that allows entities to have an
almost infinite number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

It has the ability to index, store, harvest metadata. retrieve and search
all types of files and other first class objects

%package devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the static libraries and header files needed for
developing with tracker

%package ui-tools
Summary:	Tracker search tool(s)
Group:		User Interface/Desktops
Requires:	%{name}%{?_isa} = %{version}-%{release}
Obsoletes:	paperbox <= 0.4.4
Obsoletes:	tracker-search-tool <= 0.12.0

%description ui-tools
Graphical frontend to tracker search (tracker-needle) and configuration
(tracker-preferences) facilities.

%package firefox-plugin
Summary:	A simple bookmark exporter for Tracker
Group:		User Interface/Desktops
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description firefox-plugin
This Firefox addon exports your bookmarks to Tracker, so that you can search
for them for example using tracker-needle.

%if 0%{?with_nautilus}
%package nautilus-plugin
Summary:	Tracker's nautilus plugin
Group:		User Interface/Desktops
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description nautilus-plugin
Tracker's nautilus plugin, provides 'tagging' functionality. Ability to perform
search in nautilus using tracker is built-in directly in the nautilus package.
%endif

%if 0%{?with_thunderbird}
%package thunderbird-plugin
Summary:	Thunderbird extension to export mails to Tracker
Group:		User Interface/Desktops
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description thunderbird-plugin
A simple Thunderbird extension to export mails to Tracker.
%endif

%package docs
Summary:	Documentations for tracker
Group:		Documentation
BuildArch:	noarch

%description docs
This package contains the documentation for tracker

%prep
%setup -q

%patch1 -p1 -b .onlyshowin
%patch3 -p1 -b .memory

## nuke unwanted rpaths, see also
## https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure

%build
%configure --disable-static		\
	--enable-gtk-doc		\
	--enable-miner-evolution=no	\
	--with-firefox-plugin-dir=%{_libdir}/firefox/extensions		\
%if %{with_nautilus}
	--enable-nautilus-extension					\
%else
	--disable-nautilus-extension					\
%endif
%if 0%{?with_thunderbird}
	--with-thunderbird-plugin-dir=%{_libdir}/thunderbird/extensions	\
%endif
	--with-unicode-support=libicu					\
	--disable-qt							\
	--disable-functional-tests
# Disable the functional tests for now, they use python bytecodes.

make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/tracker-1.0"	\
	> %{buildroot}%{_sysconfdir}/ld.so.conf.d/tracker-%{_arch}.conf

%if 0%{?fedora} && 0%{?fedora} < 18
desktop-file-install --delete-original			\
	--vendor="fedora"				\
	--dir=%{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}-needle.desktop
%endif

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -rf %{buildroot}%{_datadir}/tracker-tests

%find_lang %{name}

%post -p /sbin/ldconfig

%post ui-tools
touch --no-create %{_datadir}/icons/hicolor

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%postun ui-tools
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%posttrans ui-tools
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/tracker*
%{_libexecdir}/tracker*
%{_datadir}/tracker/
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_libdir}/libtracker*-1.0.so.*
%{_libdir}/tracker-1.0/
%{_libdir}/girepository-1.0/Tracker-1.0.typelib
%{_libdir}/girepository-1.0/TrackerControl-1.0.typelib
%{_libdir}/girepository-1.0/TrackerExtract-1.0.typelib
%{_libdir}/girepository-1.0/TrackerMiner-1.0.typelib
%{_mandir}/*/tracker*.gz
%{_sysconfdir}/ld.so.conf.d/tracker-%{_arch}.conf
%config(noreplace) %{_sysconfdir}/xdg/autostart/tracker*.desktop
%{_datadir}/glib-2.0/schemas/*
%exclude %{_bindir}/tracker-needle
%exclude %{_bindir}/tracker-preferences
%exclude %{_mandir}/man1/tracker-preferences.1.gz
%exclude %{_mandir}/man1/tracker-needle.1.gz

%files devel
%{_includedir}/tracker-1.0/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/vala/vapi/tracker*.*
%{_datadir}/gir-1.0/Tracker-1.0.gir
%{_datadir}/gir-1.0/TrackerControl-1.0.gir
%{_datadir}/gir-1.0/TrackerExtract-1.0.gir
%{_datadir}/gir-1.0/TrackerMiner-1.0.gir

%files ui-tools
%{_bindir}/tracker-needle
%{_bindir}/tracker-preferences
%{_datadir}/icons/*/*/apps/tracker.*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/tracker-preferences.1.gz
%{_mandir}/man1/tracker-needle.1.gz
%exclude %{_datadir}/applications/trackerbird-launcher.desktop

%files firefox-plugin
%{_datadir}/xul-ext/trackerfox/
%{_libdir}/firefox/extensions/trackerfox@bustany.org

%if 0%{?with_nautilus}
%files nautilus-plugin
%{_libdir}/nautilus/extensions-3.0/libnautilus-tracker-tags.so
%endif

%if 0%{?with_thunderbird}
%files thunderbird-plugin
%{_datadir}/xul-ext/trackerbird/
%{_libdir}/thunderbird/extensions/trackerbird@bustany.org
%{_datadir}/applications/trackerbird-launcher.desktop
%endif

%files docs
%doc docs/reference/COPYING
%{_datadir}/gtk-doc/html/libtracker-control/
%{_datadir}/gtk-doc/html/libtracker-miner/
%{_datadir}/gtk-doc/html/libtracker-sparql/
%{_datadir}/gtk-doc/html/ontology/

%changelog
* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 0.17.4-2
- 为 Magic 3.0 重建

* Sat Feb 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.17.4-1
- Update to 0.17.4

* Fri Feb 21 2014 Kalev Lember <kalevlember@gmail.com> - 0.17.3-1
- Update to 0.17.3

* Wed Feb 19 2014 Kalev Lember <kalevlember@gmail.com> - 0.17.2-2
- Make the nautilus extension conditional and disable it
- Drop the temporary compat-tracker018 subpackage

* Fri Feb 14 2014 Kalev Lember <kalevlember@gmail.com> - 0.17.2-1
- Update to 0.17.2
- Create a temporary compat-tracker018 subpackage to ease the transition
  from 0.18 ABI to 1.0

* Thu Feb 13 2014 Adam Williamson <awilliam@redhat.com> - 0.17.1-3
- rebuilt for new icu (real)

* Thu Feb 13 2014 Adam Williamson <awilliam@redhat.com> - 0.17.1-2
- rebuilt for new icu (bootstrap)

* Thu Feb 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.17.1-1
- Update to 0.17.1
- Drop upstreamed patches

* Wed Dec 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.17.0-1
- Update to 0.17.0

* Tue Dec 03 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.16.4-2
- Strengthen against sqlite failures in FTS functions (Red Hat #1026283)

* Sun Nov 24 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.4-1
- Update to 0.16.4
- Re-enable upower support

* Tue Nov 12 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.16.3-4
- Bump the minimum memory requirement to 768M (GNOME #712142)

* Mon Nov 04 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.3-3
- Unbootstrap

* Sun Nov 03 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.3-2
- Bootstrap

* Fri Nov 01 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.3-1
- Update to 0.16.3
- Build with gstreamer 1.0
- Temporarily disable upower support

* Wed Oct 30 2013 Richard Hughes <rhughes@redhat.com> - 0.16.2-5
- Rebuild for upower soname bump

* Thu Sep 19 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.2-4
- Unbootstrap

* Thu Sep 19 2013 Kalev Lember <kalevlember@gmail.com> - 0.16.2-3
- Rebuilt for totem-pl-parser soname bump

* Mon Aug 19 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.16.2-2
- Try removing the dia BuildRequires

* Sun Aug 04 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.16.2-1
- Update to 0.16.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Matthias Clasen <mclasen@redhat.com> 0.16.1-4
- Fix typos in man page
- Trim %%changelog
- Re-dethunderbirdize

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> 0.16.1-3
- Don't install a (humongous) ChangeLog file

* Wed May  8 2013 Matthias Clasen <mclasen@redhat.com> 0.16.1-2
- Make enca and libcue dependencies conditional

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> 0.16.1-1
- Update to 0.16.1

* Thu Mar 21 2013 Kalev Lember <kalevlember@gmail.com> 0.16.0-1
- Update to 0.16.0
- Remove and obsolete the tracker-miner-flickr subpackage

* Wed Feb 20 2013 Ville Skyttä <ville.skytta@iki.fi> 0.15.2-2
- Build with XPS support, fix building with GNOME keyring support.
- Be explicit about unicode=libunistring and disabling Qt.
- Description spelling fixes (BZ #902549).

* Wed Feb 20 2013 Deji Akingunola <dakingun@gmail.com> 0.15.2-1
- Update to 0.15.2 devel release

* Sat Jan 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.15.1-1
- Update to 0.15.1 devel release
- Fix up changelog dates, minor spec cleanups

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.14.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Fri Nov 02 2012 Deji Akingunola <dakingun@gmail.com> - 0.14.4-1
- Update to 0.14.4 (http://download.gnome.org/sources/tracker/0.14/tracker-0.14.4.changes)

* Thu Sep 20 2012 Deji Akingunola <dakingun@gmail.com> - 0.14.2-4
- Mark autostart desktop files as config (Gerd v. Egidy & Rex Dieter, #842318)
- Move all the files related to the Flickr miner in the '-miner-flicker' subpackage (Mathieu Bridon, #850900)

* Tue Aug 21 2012 Matthias Clasen <mclasen@redhat.com> - 0.14.2-3
- Drop obsolete BR on id3lib-devel

* Wed Aug 15 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.14.2-2
- tighten subpkg deps
- fix icon scriptlet
- -devel: drop extraneous dep on pkgconfig
- drop .desktop vendor (f18+)
- tracker should not auto-start in KDE/XFCE (#771601)

* Mon Jul 30 2012 Deji Akingunola <dakingun@gmail.com> - 0.14.2-1
- Update to 0.14.2 (http://download.gnome.org/sources/tracker/0.14/tracker-0.14.2.changes)
- Temporarily disable the evolution plugin, fails to build with evo-3.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Matthias Clasen <mclasen@redhat.com> - 0.14.1-2
- Drop the raptor-devel BR

* Sun May 20 2012 Deji Akingunola <dakingun@gmail.com> - 0.14.1-1
- Update to 0.14.1 (http://download.gnome.org/sources/tracker/0.14/tracker-0.14.1.changes)

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> - 0.14.0-4
- Rebuild (poppler-0.20.0)

* Wed May 02 2012 Milan Crha <mcrha@redhat.com> - 0.14.0-3
- Rebuild against newer evolution-data-server

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 0.14.0-2
- Silence glib-compile-schemas output in rpm scripts

* Thu Mar 08 2012 Deji Akingunola <dakingun@gmail.com> - 0.14.0-1
- Update to 0.14.0

* Mon Mar 05 2012 Dan Horák <dan[at]danny.cz> - 0.13.1-3
- Must call autoreconf because configure.ac is patched

* Mon Feb 27 2012 Deji Akingunola <dakingun@gmail.com> - 0.13.1-2
- Enable Firefox and thunderbird plugins.
- Split flickr data miner into its subpackage.

* Mon Feb 27 2012 Deji Akingunola <dakingun@gmail.com> - 0.13.1-1
- Update to 0.13.1

* Wed Feb 22 2012 Milan Crha <mcrha@redhat.com> - 0.12.10-1
- Update to 0.12.10
- Remove patch to remove g_thread_init() calls (fixed upstream)

* Wed Feb 08 2012 Milan Crha <mcrha@redhat.com> - 0.12.9-2
- Rebuild against newer evolution-data-server
- Add patch to build with evolution-3.3.5's libemail
- Add patch to remove g_thread_init() calls

* Fri Jan 27 2012 Deji Akingunola <dakingun@gmail.com> - 0.12.9-1
- Update to 0.12.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Milan Crha <mcrha@redhat.com> - 0.12.8-3
- Rebuild against newer evolution-data-server

* Tue Dec 13 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.8-2
- Apply patch to fix crash in indexing pdf (Fix by Marek Kašík; Bug #751922)

* Sun Nov 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.8-1
- 0.12.8 Release
- http://ftp.gnome.org/pub/GNOME/sources/tracker/0.12/tracker-0.12.8.news

* Tue Nov 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.7-2
- Rebuild for new e-d-s

* Mon Oct 31 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.7-1
- Update to 0.12.7
- http://ftp.gnome.org/pub/GNOME/sources/tracker/0.12/tracker-0.12.6.news
- http://ftp.gnome.org/pub/GNOME/sources/tracker/0.12/tracker-0.12.7.news

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.12.5-2
- rebuild(poppler)

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.12.5-1
- Update to 0.12.5

* Tue Oct 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.4-2
- Rebuild for new poppler 0.18

* Sun Oct 09 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.4-1
- Update to 0.12.4 stable release
- http://download.gnome.org/sources/tracker/0.12/tracker-0.12.4.changes

* Fri Sep 30 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.12.3-2
- Rebuilt for new 0.18 poppler

* Tue Sep 27 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.3-1
- Update to 0.12.3 stable release

* Fri Sep 23 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.2-1
- Update to 0.12.2 stable release
- Replace the search-tool sub-package with more appropriately named ui-tools
- Disable the search-bar until upstream redo it for GNOME 3

* Fri Sep 23 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.12.0-3
- Rebuild (poppler-0.17.3)
- Readd --enable-miner-evolution as forgotten in 0.12.0-1
- Conditionally BR libgee06-devel instead of libgee-devel for Fedora > 16

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 0.12.0-2
- Rebuild (poppler-0.17.3)

* Fri Sep 09 2011 Deji Akingunola <dakingun@gmail.com> - 0.12.0-1
- Update to 0.12.0 stable release
- Re-enable the evolution plugin

* Thu Sep  1 2011 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2
- Drop the evolution miner temporarily

* Tue Aug 30 2011 Milan Crha <mcrha@redhat.com> - 0.10.24-2
- Rebuild against newer evolution-data-server

* Thu Aug 25 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.24-1
- Update to 0.10.24
- Re-enable the evolution plugin

* Thu Aug 04 2011 Adam Williamson <awilliam@redhat.com> - 0.10.21-2
- obsolete the evo plugin as well so upgrades work

* Wed Aug 03 2011 Adam Williamson <awilliam@redhat.com> - 0.10.21-1
- complete disabling the evolution plugin

* Tue Jul 26 2011 Deji Akingunola <dakingun@gmail.com>
- Update to 0.10.21
- Temporarily disable the evolution plugin

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 0.10.15-2
- Rebuild (poppler-0.17.0)

* Tue May 31 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.15-1
- Update to 0.10.15

* Fri May 13 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.13-1
- Update to 0.10.13

* Tue Apr 26 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.10-1
- Update to 0.10.10

* Thu Apr 14 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.9-1
- Update to 0.10.9

* Tue Apr 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.8-2
- Rebuild against new gupnp-dlna, build introspection support

* Sat Apr 09 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.8-1
- Update to 0.10.8

* Sat Mar 26 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.5-1
- Update to 0.10.5

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.10.3-2
- Rebuild (poppler-0.16.3)

* Fri Mar 11 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.3-1
- Update to 0.10.3

* Thu Mar 10 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.2-1
- Update to 0.10.2

* Thu Feb 17 2011 Deji Akingunola <dakingun@gmail.com> - 0.10.0-1
- Update to 0.10.0
- Re-enable tracker-search-bar

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.9.37-3
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.37-1
- Update to 0.9.37
- Disable tracker-search-bar - building it is currently failing with gtk3

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.36-2
- Rebuild against newer gtk

* Tue Feb 01 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.36-1
- Update to 0.9.36
- Temporarily disable the docs subpackage

* Tue Jan 25 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.35-1
- Update to 0.9.35
- Re-enable gupnp-dlna support 

* Tue Jan 11 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.33-3
- Temporarily disable gupnp-dlna.
- Update nautilus extensions directory for nautilus-3.x.

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.33-2
- Rebuild against newer gtk

* Tue Jan 04 2011 Deji Akingunola <dakingun@gmail.com> - 0.9.33-1
- Update to 0.9.33
- Substitute gdk-pixbuf for qt4 as music album extractor
- Split off nautilus-plugin into a sub-package

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.9.30-3
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.30-2
- rebuild (poppler)

* Sat Dec 04 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.28-1
- Update to 0.9.30

* Sun Nov 07 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.27-1
- Update to 0.9.27

* Tue Oct 12 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.24-2
- Rebuild for evolution-data-server-2.91.0.

* Fri Oct 08 2010 Deji Akingunola <dakingun@gmail.com> - 0.9.24-1
- First update to 0.9.x series
- Re-word the package summary (conformant to upstream wording).

* Tue Sep 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-3
- Rebuild for poppler-0.15.

* Tue Sep 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-2
- Rebuild for evolution (camel) update.
- Apply patch to build with gtk >= 2.90.7

* Thu Sep 02 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.17-1
- Update to 0.8.17 release

* Fri Aug 20 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.16-1
- Update to 0.8.16 release

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.15-2
- rebuild (poppler)

* Fri Jul 16 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.15-1
- Update to 0.8.15 release
- Package the docs licensing file
- Patch for EDS API changes (Migrate from CamelException to GError)
- Backport a memory leak fix

* Mon Jun 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.13-1
- Update to 0.8.13 release

* Tue Jun 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.8.11-2
- Rebuild against new poppler

* Tue Jun 15 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.11-1
- Update to 0.8.11 release
- Adapt to EDS Camel API changes (Convert CamelObject events to GObject signals), patch not tested yet.

* Thu May 27 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.9-1
- Update to 0.8.9 release

* Thu May 06 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.5-1
- Update to 0.8.5 release
- Provide an upgrade path for paperbox (make ~-search-tool obsolete it) on F-13.
- Patch to build with eds-2.31.1 (Camel headers locked down)

* Thu Apr 29 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.4-1
- Update to 0.8.4 release

* Mon Apr 19 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.2-1
- Update to 0.8.2 release

* Thu Apr 01 2010 Deji Akingunola <dakingun@gmail.com> - 0.8.0-1
- Update to 0.8.0 release

* Thu Mar 25 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.28-1
- Update to 0.7.28 release

* Thu Mar 11 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.25-1
- Update to 0.7.25 release

* Tue Mar 02 2010 Deji Akingunola <dakingun@gmail.com> - 0.7.23-1
- Update to 0.7.23 release

* Sat Aug 29 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.95-4
- Explicitly require apps needed in the text filters of common documents (Fedora bug #517930)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.95-2
- Ship the manpages in the appropriate sub-packages (Fedora bug #479278)

* Fri May 22 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.95-1
- Update to 0.6.95 release

* Fri May 01 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.94-1
- Update to 0.6.94 release

* Thu Apr 09 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.93-1
- Update to 0.6.93 release

* Sat Mar 28 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.92-1
- Update to 0.6.92 release

* Fri Mar 13 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.91-1
- Update to 0.6.91 release

* Mon Feb 09 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.90-1
- New release, with tons of changes

* Tue Dec 23 2008 - Caolán McNamara <caolanm@redhat.com> - 0.6.6-10
- make build

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-9
- Add libtool BR

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-8
- Update patch to actually apply, way to do releases often

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-7
- Add patch to port to GMime 2.4

* Wed Dec 10 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6.6-6
- Rebuild for gmime dependency

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.6-5
- Rebuild for Python 2.6

* Fri Nov 28 2008 Caolán McNamara <caolanm@redhat.com> - 0.6.6-4
- rebuild for dependancies

* Thu Jun 05 2008 Caolán McNamara <caolanm@redhat.com> - 0.6.6-3
- rebuild for dependancies

* Fri Mar 14 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.6-2
- BR poppler-glib-devel instead of poppler-devel for pdf extract module (Thanks to Karsten Hopp mass rebuild work for bringing this to light)

* Sun Mar 02 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.6-1
- New release 0.6.6

* Thu Feb 28 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.5-1
- New release 0.6.5

* Fri Feb 22 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-7
- Ship the tracker-applet program in the tracker-search-tool subpackage
  (Bug #434551)

* Sun Feb 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-6
- Rebuild for gcc43

* Thu Jan 24 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-5
- Backport assorted fixes from upstream svn (Fix Fedora bug 426060)

* Mon Jan 21 2008 Deji Akingunola <dakingun@gmail.com> - 0.6.4-4
- Now require the externally packaged o3read to provide o3totxt

* Fri Dec 14 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.4-3
- Undo the patch, seems to be issues (bug #426060)

* Fri Dec 14 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.4-2
- Backport crasher fixes from upstream svn trunk

* Tue Dec 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.4-1
- Version 0.6.4

* Tue Dec 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.3-3
- Rebuild for exempi-1.99.5

* Sun Nov 25 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.6.3-2
- Add missing gtk+ icon cache scriptlets.

* Tue Sep 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.3-1
- Version 0.6.3

* Tue Sep 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.2-2
- Make trackerd start on x86_64 (Bug #286361, fix by Will Woods)

* Wed Sep 05 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.2-1
- Version 0.6.2

* Sat Aug 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.1-2
- Rebuild

* Wed Aug 08 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.0-3
- License tag update

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.6.0-2.1
- rebuild for toolchain bug

* Mon Jul 23 2007 Deji Akingunola <dakingun@gmail.com> - 0.6.0-1
- Update to 0.6.0
- Manually specify path to deskbar-applet handler directory, koji can't find it

* Mon Jan 29 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-2
- Split out tracker-search-tool sub-packages, for the GUI facility
- Add proper requires for the -devel subpackage
- Deal with the rpmlint complaints on rpath

* Sat Jan 27 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Tue Dec 26 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.3-1
- Update to 0.5.3

* Mon Nov 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.2-2
- Apply patch on Makefile.am instead of Makefile.in
- Add libtool to BR

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.2-1
- Update to 0.5.2

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.1-1
- Update to new version

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-7
- Have the devel subpackage require pkgconfig
- Make the description field not have more than 76 characters on a line
- Fix up the RPM group

* Mon Nov 06 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-6
- Explicitly require dbus-devel and dbus-glib (needed for FC < 6) 

* Sun Nov 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-5
- Remove unneeded BRs (gnome-utils-devel and openssl-devel) 

* Sun Nov 05 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-4
- Add autostart desktop file.
- Edit the package description as suggested in review

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-3
- More cleaups to the spec file.

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-2
- Add needed BRs

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.5.0-1
- Initial packaging for Fedora Extras
