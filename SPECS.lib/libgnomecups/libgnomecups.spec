Summary:  GNOME library for CUPS integration
Name:     libgnomecups
Version:  0.2.3
Release:  15%{?dist}
License:  LGPLv2
Group:    Development/Libraries
URL:      http://www.gnome.org
Requires: cups-libs
Requires: dbus-glib
BuildRequires: cups-devel
BuildRequires: glib2-devel
BuildRequires: gnutls-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: gnome-common
BuildRequires: autoconf, automake, libtool, gettext
BuildRequires: intltool
Source: http://ftp.gnome.org/pub/gnome/sources/libgnomecups/0.2/%{name}-%{version}.tar.bz2
#Fedora specific patches
Patch3: libgnomecups-dbus.patch
Patch5: libgnomecups-0.1.14-go-direct.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=520449
Patch6: libgnomecups-lpoptions.patch
Patch7: libgnomecups-glib-header.patch
Patch8: libgnomecups-0.2.3-g_list_find_custom.patch
Patch9: libgnomecups-0.2.3-pkgconfig.patch 
Patch10: libgnomecups-0.2.3-cups-1.6.patch

%description
GNOME library for CUPS integration

%package devel
Summary: GNOME library for CUPS integration
Group:  Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: cups-devel glib2-devel

%description devel
GNOME library for CUPS integration

%prep
%setup -q
%patch3 -p1 -b .dbus
%patch5 -p1 -b .go-direct
%patch6 -p1 -b .lpoptions
%patch7 -p1 -b .glib-header
%patch8 -p1
%patch9 -p0
%patch10 -p1

%build
autoreconf -f -i
%configure --with-dbus=yes --disable-static
make  %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc NEWS AUTHORS COPYING.LIB
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.3-15
- 为 Magic 3.0 重建

* Tue Nov 27 2012 Liu Di <liudidi@gmail.com> - 0.2.3-14
- 为 Magic 3.0 重建

* Tue Nov 27 2012 Liu Di <liudidi@gmail.com> - 0.2.3-13
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Marek Kasik <mkasik@redhat.com> - 0.2.3-10
- Fix build by including glib.h alone

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 09 2010 Parag Nemade <paragn AT fedoraproject.org> 0.2.3-8
- Merge-review cleanup (#226013)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.2.3-6
- Drop cups, dbus dependencies (#192402)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct  1 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-4
- Make it build

* Tue Mar  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-3
- Honor cups user default options from ~/.cups/lpoptions

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.3-2
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.2.2-12
- Rebuild against new dbus-glib

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.2.2-11
- Rebuild

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.2.2-10
- Update license field

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.2.2-9
- Don't ship static libraries
- Small spec file cleanups

* Mon Oct  2 2006 Christopher Aillon <caillon@redhat.com> - 0.2.2-8
- Add fixes for a leak and an invalid memory access from usptream.

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.2.2-7
- Rebuild against new dbus

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2.2-6.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 0.2.2-6
- rebuilt with new gnutls

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> - 0.2.2-5
- More BuildRequires

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 0.2.2-4
- Patch from n0dalus <n0dalus+redhat@gmail.com> - add build requires

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.2-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.2.2-3
- rebuild for new dbus

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 0.2.2-2
- rebuilt against new openssl

* Wed Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Wed Apr 13 2005 David Zeuthen <davidz@redhat.com> - 0.2.0-2
- Fix Requires for -devel package (#152500)

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 0.2.0-1
- New upstream version; drop patches that are upstreamed

* Fri Mar  4 2005 John (J5) Palmieri <johnp@redhat.com> 0.1.14-3
- edit dbus patch - don't free const variable

* Wed Mar  2 2005 Jindrich Novy <jnovy@redhat.com> 0.1.14-2
- rebuilt

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> 0.1.14-1
- Update to 0.1.14

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 0.1.13-1
- New upstream version

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 0.1.12-5
- Add patch which tries to avoid blocking the main loop in
  certain cases

* Thu Sep 30 2004 Colin Walters <walters@redhat.com> 0.1.12-4
- Change group to Development/Libraries (131688)

* Thu Sep 30 2004 Colin Walters <walters@redhat.com> 0.1.12-3
- Pass --with-dbus=yes to configure to be extra sure
- Add libgnomecups-no-gnome-common.patch
- autoreconf to pick up configure changes

* Thu Sep 30 2004 Colin Walters <walters@redhat.com> 0.1.12-2
- Pass --with-dbus to configure
- BuildRequire dbus-devel

* Thu Sep 13 2004 Colin Walters <walters@redhat.com> 0.1.12-1
- New upstream release
- Remove upstreamed thread-init patch  
- Remove upstreamed async-printers patch  
- Actually apply DBus patch

* Thu Sep 09 2004 Colin Walters <walters@redhat.com> 0.1.11-5
- Use DBus to get notifications of new printers.

* Fri Sep 03 2004 Matthias Clasen <mclasen@redhat.com> 0.1.11-4
- Make updating the printer list async.

* Tue Aug 31 2004 Matthias Clasen <mclasen@redhat.com> 0.1.11-3
- Fix some issues with the async ppd patch

* Fri Aug 27 2004 Matthias Clasen <mclasen@redhat.com> 0.1.11-2
- Update async ppd patch and apply it

* Tue Aug 24 2004 Colin Walters <walters@redhat.com> 0.1.11-1
- New upstream version
- Remove upstreamed patch libgnomecups-path-escape.patch
- Add thread init patch
- Do not actually apply ppd async patch yet

* Wed Aug 18 2004 Colin Walters <walters@redhat.com> 0.1.10-1
- Update to 0.1.10
- Remove upstreamed patch libgnomecups-0.1.9-error.patch
- Remove upstreamed patch libgnomecups-0.1.9-get-attributes-from-host.patch
- Remove upstreamed patch libgnomecups-0.1.9-notify-remove.patch
- Remove upstreamed patch libgnomecups-0.1.9-attributes.patch

* Sat Aug 14 2004 Colin Walters <walters@redhat.com> 0.1.9-3
- Add patch to not poll individual printer jobs
- Add patch to fix printer attribute retrieval (API change)

* Fri Jul 30 2004 Colin Walters <walters@redhat.com> 0.1.9-2
- Add patch to get attributes from correct host
- Add patch to fix error freeing
- Purge all sorts of useless comments from this file

* Wed Jul 28 2004 Colin Walters <walters@redhat.com> 0.1.9-1
- Update to 0.1.9
- Remove includes patch

* Mon Jun 21 2004 Colin Walters <walters@redhat.com> 0.1.8.cvs20040621-2
- Apply little patch to fix inclues

* Mon Jun 21 2004 Colin Walters <walters@redhat.com> 0.1.8.cvs20040621-1
- Update to latest CVS, which includes shiny new async patches
- Remove libgnomecups-host.patch, incorporated upstream

* Fri Jun 18 2004 Matthias Clasen <mclasen@redhat.com> 0.1.8.cvs20040618-1
- Update to latest CVS
- Remove some patches

* Wed Jun 15 2004 Colin Walters <walters@redhat.com> 0.1.8.cvs20040615-1
- Update to latest CVS
- Apply Matthias's patches

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 0.1.6.cvs20040602-2
- rebuilt

* Wed Jun 02 2004 Colin Walters <walters@redhat.com> 0.1.6.cvs20040602-1
- Update to latest CVS
- Include Matthias' and my patch that makes remote queues
  work, etc.

* Wed Apr 28 2004 Dan Williams <dcbw@redhat.com> 0.1.6-7
- Add "cups-devel" to the libgnomecups-devel package Requires

* Thu Mar  4 2004 Bill Nottingham <notting@redhat.com> 0.1.6-6
- remove comment to avoid postun warning

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Dan Williams <dcbw@redhat.com> 0.1.6-4
- Augment NVR to differentiate Fedora Core/RHEL

* Thu Jan 22 2004 Dan Williams <dcbw@redhat.com> 0.1.6-3
- Bump for rebuild into Fedora Core 2

* Wed Dec 03 2003 Dan Williams <dcbw@redhat.com>
- Initial Red Hat RPM release.

* Sat Nov 01 2003 RunNHide <runnhide@runnhide.cjb.net>
- Initial RPM release for Fedora and Rawhide.
