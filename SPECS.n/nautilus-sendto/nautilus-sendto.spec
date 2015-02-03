Name:           nautilus-sendto
Epoch:          1
Version:	3.8.2
Release:        1%{?dist}
Summary:        Nautilus context menu for sending files
Summary(zh_CN.UTF-8): Nautilus 发送文件的右键菜单

Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
License:        GPLv2+
URL:            ftp://ftp.gnome.org/pub/gnome/sources/%{name}
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/%{name}/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  perl-XML-Parser intltool

# For compat with old nautilus-sendto packaging
Provides: nautilus-sendto-gaim
Obsoletes: nautilus-sendto-bluetooth
Provides: nautilus-sendto-bluetooth
Obsoletes: nautilus-sendto-devel < 1:3.7.92

%description
The nautilus-sendto package provides a Nautilus context menu for
sending files via other desktop applications.  These functions are
implemented as plugins, so nautilus-sendto can be extended with
additional features.

%description -l zh_CN.UTF-8
Nautilus 发送文件的右键菜单。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -name '*.a' -o -name '*.la' \) -exec rm -f {} \;
magic_rpm_clean.sh
%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog ChangeLog.pre-1.1.4.1 COPYING NEWS
%{_bindir}/nautilus-sendto
%{_mandir}/man1/nautilus-sendto.1.gz

%changelog
* Wed Jan 21 2015 Liu Di <liudidi@gmail.com> - 1:3.8.2-1
- 更新到 3.8.2

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.8.0-1
- Update to 3.8.0

* Thu Mar 21 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.92-1
- Update to 3.7.92

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.1-1
- Update to 3.6.1

* Tue Nov 20 2012 Milan Crha <mcrha@redhat.com> - 1:3.6.0-3
- Rebuild against newer evolution-data-server

* Thu Oct 25 2012 Milan Crha <mcrha@redhat.com> - 1:3.6.0-2
- Rebuild against newer evolution-data-server

* Wed Sep 26 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.0-1
- Update to 3.6.0

* Wed Aug 22 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:3.5.3-4
- Drop old GConf bits. Fedora versions that needed this haven't been supported for awhile.

* Tue Aug 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1:3.5.3-3
- Rebuild for new libcamel.

* Tue Jul 17 2012 Paul W. Frields <stickster@gmail.com> - 1:3.5.3-2
- Rebuild for newer libcamel

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.3-1
- Update to 3.5.3

* Fri May 11 2012 Bastien Nocera <bnocera@redhat.com> 3.0.3-1
- Update to 3.0.3

* Mon Apr 30 2012 Paul W. Frields <stickster@gmail.com> - 1:3.0.2-3
- Rebuild against newer evolution-data-server

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.0.2-2
- Silence rpm scriptlet output

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.0.2-1
- Update to 3.0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.1-3
- Rebuild

* Mon Oct 24 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:3.0.1-2
- Rebuld against libcamel.

* Mon Sep 26 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-1
- Update to 3.0.1

* Tue Sep 06 2011 Brian Pepple <bpepple@fedoraproject.org> - 1:3.0.0-12
- Rebuld against new libcamel.

* Tue Aug 30 2011 Milan Crha <mcrha@redhat.com> - 1:3.0.0-11
- Rebuild against newer evolution-data-server (once again)

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 1:3.0.0-10
- Rebuild against newer evolution-data-server

* Fri Aug 19 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-9
- Try again to rebuild

* Tue Aug 16 2011 Paul W. Frields <stickster@gmail.com> - 1:3.0.0-7
- Rebuild for new e-d-s

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-6
- Rebuild

* Tue Jul 05 2011 Adam Williamson <awilliam@redhat.com> - 3.0.0-5
- rebuild for new e-d-s

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> 3.0.0-4
- rebuild for new gupnp/gssdp

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-3
- Another rebuild

* Tue May 10 2011 Paul W. Frields <stickster@gmail.com> - 3.0.0-2
- Rebuild for new libcamel

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Mon Feb 21 2011 Bastien Nocera <bnocera@redhat.com> 2.91.6-1
- Update to 2.91.6

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 2.90.0-13
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.90.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.90.0-11
- Rebuild against newer gtk

* Tue Feb  1 2011 Christopher Aillon <caillon@redhat.com> 2.90.0-10
- Rebuild against newer e-d-s

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.90.0-9
- Rebuild against newer evolution

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.90.0-8
- Rebuild against new gtk

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-7
- Drop extension, now part of nautilus

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-6
- Co-own /usr/share/gtk-doc (#604405)

* Thu Aug 05 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-5
- Update requires for new epoch

* Wed Aug 04 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-4
- Up Epoch for F-14 changes

* Thu Jul 15 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-3
- Rebuild against new evolution-data-server

* Wed Jun 30 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-2
- Remove outdated BuildRequires

* Tue Jun 29 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-1
- Update to 2.90.0

* Tue Jun 15 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.4-4
- Rebuild again

* Wed May 26 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.28.4-3
- Rebuild for new eds.

* Fri May  7 2010 Brian Pepple <bpepple@fedoraproject.org> - 2.28.4-2
- Rebuild for new eds.
- Remove empathy-devel BR. Empathy doesn't ship devel files anymore.

* Mon Mar 29 2010 Bastien Nocera <bnocera@redhat.com> 2.28.4-1
- Update to 2.28.4

* Mon Mar 15 2010 Bastien Nocera <bnocera@redhat.com> 2.28.3-1
- Update to 2.28.3

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> 2.28.2-3
- Fix a directory ownership issue

* Mon Nov 30 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-2
- Remove bluetooth plugin, it's now in gnome-bluetooth

* Tue Nov 17 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-1
- Update to 2.28.2
- Add devel sub-package
- Remove unneeded pidgin and gajim BRs

* Mon Sep 21 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-1
- Update to 2.28.0

* Fri Sep 18 2009 Caolán McNamara <caolanm@redhat.com> - 1.1.7-3
- rebuild for dependencies

* Tue Sep  8 2009 Brian Pepple <bpepple@fedoraproject.org> - 1.1.7-2
- Rebuild for new Empathy.

* Wed Sep 02 2009 Bastien Nocera <bnocera@redhat.com> 1.1.7-1
- Update to 1.1.7

* Wed Aug 26 2009 Brian Pepple <bpepple@fedoraproject.org> - 1.1.6-3
- Rebuild for new Empathy.

* Thu Jul 30 2009 Bastien Nocera <bnocera@redhat.com> 1.1.6-2
- Rebuild for new empathy

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 1.1.6-1
- Update to 1.1.6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Bastien Nocera <bnocera@redhat.com> 1.1.5-4
- Update for new empathy API

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> 1.1.5-3
- Rebuild against newer empathy

* Tue May 05 2009 Bastien Nocera <bnocera@redhat.com> 1.1.5-2
- Disable the evolution plugin, it will be in Evo itself in 2.27.x
  See http://bugzilla.gnome.org/show_bug.cgi?id=579099

* Tue May 05 2009 Bastien Nocera <bnocera@redhat.com> 1.1.5-1.1
- Update to 1.1.5

* Tue Apr 28 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4.1-2
- Build with gajim support (#497975)

* Mon Apr 20 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4.1-1
- Update to 1.1.4.1

* Fri Apr 17 2009 Karsten Hopp <karsten@redhat.com> 1.1.4-1.1
- don't require pidgin-* on s390, s390x as that has ExcludeArch s390(x)

* Fri Apr 17 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-1
- Update to 1.1.4

* Fri Apr 03 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 1.1.2-4
- Make build and run with current Empathy

* Wed Mar 04 2009 Warren Togami <wtogami@redhat.com> - 1.1.2-3
- rebuild for libempathy

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Tue Feb 17 2009 Paul W. Frields <stickster@gmail.com> - 1.1.1-3
- Rebuild for dependencies

* Thu Feb 12 2009 - Caolán McNamara <caolanm@redhat.com> - 1.1.1-2
- rebuild for dependencies

* Sat Jan 10 2009 - Bastien Nocera <bnocera@redhat.com> - 1.1.1
- Update to 1.1.1
- Add UPNP and Empathy plugins

* Tue Sep 23 2008 - Bastien Nocera <bnocera@redhat.com> - 1.1.0
- Update to 1.1.0

* Wed Jul 23 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.1
- Update to 1.0.1

* Thu Jun 12 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.0
- Update to 1.0.0

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-4
- Rebuild again

* Tue May 13 2008 - Bastien Nocera <bnocera@redhat.com> - 0.14.0-3
- Rebuild

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-2
- Fix source url

* Thu Mar 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Thu Feb 07 2008 - Bastien Nocera <bnocera@redhat.com> - 0.13.2-1
- Update to 0.13.2

* Mon Jan 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Sun Jan 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.13-1
- Update to 0.13

* Fri Dec 28 2007 Adel Gadllah <adel.gadllah@gmail.com> - 0.12-7
- Fix icq file transfers with pidgin RH #408511

* Wed Dec 26 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-6
- Install the nautilus exension in the right spot

* Mon Nov 19 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-5
- Fix the pidgin plugin to work with libpurple (#389121)

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-4
- Rebuild against new dbus-glib

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.12-3
- Rebuild

* Mon Aug 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.12-2
- Fix the Thunderbird patch to apply properly

* Mon Aug 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.12-1
- Update to 0.12 and drop obsolete patches

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-5
- Update the license field

* Fri May 11 2007 Stu Tomlinson <stu@nosnilmot.com> - 0.10-4
- Update to work with pidgin

* Wed May  9 2007 Matthias Clasen <mclasen@redhat.com> - 0.10-3
- Fix a problem with dbus error handling  (#239588)

* Mon Apr 16 2007 Warren Togami <wtogami@redhat.com> - 0.10-2
- disable gaim dep temporarily during transition to pidgin

* Sun Mar 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10-1
- Update to 0.10, as 0.9 didn't compile

* Fri Mar 09 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9-1
- Update to 0.9
- Remove the bluetooth subpackage, it only depends on
  gbus-glib now

* Tue Jan 23 2007 Alexander Larsson <alexl@redhat.com> - 0.8-4
- Rebuild against new gaim (#223765)

* Wed Nov 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-3
- Rebuild against new libbtctl

* Fri Oct 27 2006 Matthew Barnes <mbarnes@redhat.com> - 0.8-2
- Update BuildRequires for evolution-data-server-devel.
- Rebuild against evolution-data-server-1.9.1.

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Upgrade to 0.8

* Sat Sep 16 2006 Matthias Clasen <mclasen@redhat.com> - 0.7-5
- Include Thunderbird support and make it work
- Add missing BRs

* Mon Aug 14 2006 Alexander Larsson <alexl@redhat.com> - 0.7-4
- Buildrequire nautilus-devel

* Thu Aug 10 2006 Alexander Larsson <alexl@redhat.com> - 0.7-3
- Make nautilus-sendto-bluetooth require gnome-bluetooth (#201908)

* Sat Aug 05 2006 Caolan McNamara <caolanm@redhat.com> - 0.7-2
- rebuild against new e-d-s

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7-1.1
- rebuild

* Tue Jul 11 2006 Matthias Clasen  <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Wed Jun 14 2006 Alexander Larsson <alexl@redhat.com> - 0.5-4
- Rebuild again, hopefully fixing libbluetooth issue

* Mon Jun 12 2006 Alexander Larsson <alexl@redhat.com> - 0.5-3
- Rebuild for new libbluetooth soname

* Sat Jun 10 2006 Matthias Clasen <mclasen@redhat.com> 0.5-2
- Add missing BuildRequires

* Mon May 22 2006 Alexander Larsson <alexl@redhat.com> 0.5-1
- Update to 0.5
- Add libgnomeui-devel buildreq

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.4-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.4-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Jan 28 2006 David Malcolm <dmalcolm@redhat.com> 0.4-7
- rebuild for new e-d-s

* Tue Dec 20 2005 Alexander Larsson <alexl@redhat.com> 0.4-6
- Rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Alexander Larsson <alexl@redhat.com> - 0.4-5
- Build in Core
- Move gaim plugin into main package
- Fix up some build requirements
- No bluetooth on s390*

* Sat Oct  8 2005 Paul W. Frields <stickster@gmail.com> - 0.4-4
- Eliminate superfluous Requires

* Sat Oct  8 2005 Paul W. Frields <stickster@gmail.com> - 0.4-3
- Rearrange Requires and BuildRequires for subpackages
- Include default Evolution plugin in main package

* Fri Oct  7 2005 Paul W. Frields <stickster@gmail.com> - 0.4-2
- Use appropriate BuildRequires for nautilus and gaim

* Fri Oct  7 2005 Paul W. Frields <stickster@gmail.com> - 0.4-1
- Initial version
