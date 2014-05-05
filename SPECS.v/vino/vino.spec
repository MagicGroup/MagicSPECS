%define libgcrypt_version 1.2.0
%define libnotify_version 0.7.0
%define telepathy_glib_version 0.11.6

Summary: A remote desktop system for GNOME
Name: vino
Version: 3.11.4
Release: 2%{?dist}
URL: http://www.gnome.org
#VCS: git:git://git.gnome.org/vino
Source0: http://download.gnome.org/sources/vino/3.11/%{name}-%{version}.tar.xz

License: GPLv2+
Group: User Interface/Desktops

BuildRequires: gtk3-devel
BuildRequires: libgcrypt-devel >= %{libgcrypt_version}
BuildRequires: libnotify-devel >= %{libnotify_version}
BuildRequires: telepathy-glib-devel >= %{telepathy_glib_version}
BuildRequires: libXt-devel, libXtst-devel, libXdamage-devel
BuildRequires: pkgconfig(avahi-client) pkgconfig(avahi-glib)
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libsecret-devel
BuildRequires: libsoup-devel
BuildRequires: NetworkManager-devel
BuildRequires: libSM-devel
# BuildRequires: autoconf automake libtool
BuildRequires: gnome-common

%description
Vino is a VNC server for GNOME. It allows remote users to
connect to a running GNOME session using VNC.

%prep
%setup -q

# autoreconf -i -f
# intltoolize --force

%build
%configure                      \
  --disable-http-server         \
  --disable-silent-rules        \
  --with-avahi                  \
  --with-network-manager        \
  --with-secret                 \
  --with-telepathy              \
  --with-gnutls                 \

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README docs/TODO docs/remote-desktop.txt
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Vino.service
%{_datadir}/telepathy/clients/Vino.client
%{_libexecdir}/*
%{_sysconfdir}/xdg/autostart/vino-server.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.Vino.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Vino.gschema.xml
%{_datadir}/GConf/gsettings/org.gnome.Vino.convert

%changelog
* Sun May 04 2014 Liu Di <liudidi@gmail.com> - 3.11.4-2
- 为 Magic 3.0 重建

* Mon Jan 13 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Thu Sep 26 2013 Rex Dieter <rdieter@fedoraproject.org> 3.10.0-2
- add explicit avahi build deps, build verbosely.

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2
- Adapt the spec file for dropped preferences dialog
- Build with libsecret
- Update the configure options; most have been renamed from --enable to --with

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Fri Mar  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Sun Dec  2 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.2-2
- Don't add a vendor prefix to the desktop file, that breaks
  activating the preferences from the statusicon (#827913)

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92
- Don't BR unique-devel; vino doesn't use libunique any more

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Tue Jul 05 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.2-2
- Update icon cache scriptlet

* Wed May  4 2011 Christopher Aillon <caillon@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.5-1
- Update to 2.99.5

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.4-1
- Update to 2.99.4

* Tue Mar  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.3-1
- Update to 2.99.3

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.0-1
- Update to 2.99.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-2
- Rebuild against libnotify 0.7.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.4-1
- Update to 2.31.4

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Sun Sep 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Even better, just rely on autostart

* Sun Sep 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Make vino-server set a proper restart command

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-2
- Enable telepathy

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-5
- Rebuild to shrink GConf schemas

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-4
- Try again: rebuild with new gcc

* Mon Jun 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-3
- Rebuild with new gcc

* Fri Jun 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-2
- Drop unneeded direct dependencies

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/vino/2.26/vino-2.26.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92
- Enable NetworkManager support

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Fri Jan 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Fri Jul 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-3
- Use autostart to have gnome-session start the server

* Fri Jul 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Use standard icon names

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update 2.21.92

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Wed Dec  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-2
- Rebuild against new dbus-glib

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (translation updates)

* Tue Oct  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Fix a directory ownership issue

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90
- Update the license field

* Mon Jul  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92
- Drop obsolete patches

* Wed Jan 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-2
- Fix some careless gconf value handling
- use libnotify
- Improve category in the desktop file

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Mon Nov  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Sat Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-6
- Fix scripts according to the packaging guidelines

* Tue Oct 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-5
- Fix #191160

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5-4.1
- rebuild

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-4
- More missing BuildRequires

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.5-3
- Add missing BuildRequires

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Mark McLoughlin <markmc@redhat.com> 2.13.5-2
- Build with --enable-avahi

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 26 2005 Mark McLoughlin <markmc@redhat.com> 2.12.0-2
- Add patch from Alexandre Oliva <oliva@lsd.ic.unicamp.br> to fix
  more keyboard brokeness (#158713)

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Wed Aug 17 2005 Matthias Clasen <mclasen@redhat.com> 2.11.90-2
- Rebuild

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> 2.11.90-1
- New upstream version

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 2.11.1.2-1
- Newer upstream version
- Drop upstreamed patches

* Fri May 20 2005 Mark McLoughlin <markmc@redhat.com> 2.10.0-4
- Fix various keyboarding handling issues:
   + bug #142974: caps lock not working
   + bug #140515: shift not working with some keys
   + bug #134451: over-eager key repeating

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 2.10.0-3
- silence %%post

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 2.10.0-1
- Update to 2.10.0
- Update the GTK+ theme icon cache on (un)install

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 2.9.2-2
- Rebuild with gcc4

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> 2.9.2-1
- Update to 2.9.2

* Tue Oct 12 2004 Mark McLoughlin <markmc@redhat.com> 2.8.1-1
- Update to 2.8.1
- Remove backported fixes

* Thu Oct  7 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0.1-1.1
- Don't hang with metacity's "reduced resources" mode (#134240) 
- Improve the key repeat rate situation a good deal (#134451)

* Wed Sep 29 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0.1-1
- Update to 2.8.0.1

* Tue Sep 21 2004 Mark McLoughlin <markmc@redhat.com> 2.8.0-1
- Update to 2.8.0
- Remove upstreamed work-without-gnutls patch

* Tue Sep  7 2004 Matthias Clasen <mclasen@redhat.com> 2.7.92-3
- Disable help button until there is help (#131632)
 
* Wed Sep  1 2004 Mark McLoughlin <markmc@redhat.com> 2.7.92-2
- Add patch to fix hang without GNU TLS (bug #131354)

* Mon Aug 30 2004 Mark McLoughlin <markmc@redhat.com> 2.7.92-1
- Update to 2.7.92

* Tue Aug 17 2004 Mark McLoughlin <markmc@redhat.com> 2.7.91-1
- Update to 2.7.91

* Mon Aug 16 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-2
- Define libgcrypt_version

* Thu Aug 12 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 2.7.4-1
- Update to 2.7.4

* Tue Jul 13 2004 Mark McLoughlin <markmc@redhat.com> 2.7.3.1-1
- Initial build.
