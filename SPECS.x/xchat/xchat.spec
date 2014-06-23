%define _default_patch_fuzz 2
%define gconf_version 2.14

Summary:   A popular and easy to use graphical IRC (chat) client
Name:      xchat
Version:   2.8.8
Release:   13%{?dist}
Epoch:     1
Group:     Applications/Internet
License:   GPLv2+
URL:       http://www.xchat.org
Source:    http://www.xchat.org/files/source/2.8/xchat-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Patches 0-9 reserved for official xchat.org patches

Patch12: xchat-1.8.7-use-sysconf-to-detect-cpus.patch
# see #241923
Patch35: xchat-2.8.4-disable-tray-icon-by-default.patch
# Upstream XChat 2.8.6 defaults to Latin1 (what upstream calls the "IRC"
# encoding). Default to UTF-8 instead (as previous versions did, at least when
# running under a UTF-8 locale).
# Both the "IRC" and "UTF-8" settings will try to accept both Latin1 and UTF-8
# when it comes in, however "IRC" sends Latin1, "UTF-8" sends UTF-8.
Patch41: xchat-2.8.6-default-utf8.patch
# patch to add ability to change to tab with most recent activity
# See http://sourceforge.net/tracker/?func=detail&aid=2022871&group_id=239&atid=350239
Patch50: xchat-2.8.6-change-page-activity.patch
# add port numbers for Freenode (Debarshi Ray)
Patch51: xchat-2.8.6-freenode-ports.patch
# work with libnotify 0.7
# https://sourceforge.net/tracker/?func=detail&aid=3109838&group_id=239&atid=100239
Patch52: xchat-2.8.8-libnotify07.patch
# link against libnotify
# https://sourceforge.net/tracker/?func=detail&aid=3280223&group_id=239&atid=100239
Patch53: xchat-2.8.8-link-against-libnotify.patch

Patch54: xchat-2.8.8-glib.patch

BuildRequires: perl perl(ExtUtils::Embed) python-devel openssl-devel pkgconfig, tcl-devel
BuildRequires: GConf2-devel
BuildRequires: dbus-devel >= 0.60, dbus-glib-devel >= 0.60
BuildRequires: glib2-devel >= 2.10.0, gtk2-devel >= 2.10.0, bison >= 1.35
BuildRequires: gettext /bin/sed
BuildRequires: libtool
BuildRequires: libntlm-devel
BuildRequires: libsexy-devel
BuildRequires: desktop-file-utils >= 0.10
BuildRequires: libnotify-devel
# For xchat-2.8.8-link-against-libnotify.patch
BuildRequires: autoconf
# For gconftool-2:
Requires(post): GConf2 >= %{gconf_version}
Requires(preun): GConf2 >= %{gconf_version}

# For aplay:
Requires: alsa-utils

# Ensure that a compatible libperl is installed
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Provides: xchat-perl = %{epoch}:%{version}-%{release}
Obsoletes: xchat-perl < %{epoch}:%{version}-%{release}
Provides: xchat-python = %{epoch}:%{version}-%{release}
Obsoletes: xchat-python < %{epoch}:%{version}-%{release}

%description
X-Chat is an easy to use graphical IRC chat client for the X Window System.
It allows you to join multiple IRC channels (chat rooms) at the same time, 
talk publicly, private one-on-one conversations etc. Even file transfers
are possible.

This includes the plugins to run the Perl and Python scripts.

%package tcl
Summary: Tcl script plugin for X-Chat
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%description tcl
This package contains the X-Chat plugin providing the Tcl scripting interface.

%prep
%setup -q
# Various small fixes from CVS that are considered safe to apply to 2.8.6.
# (currently none)

%patch12 -p0 -b .use-sysconf-to-detect-cpus
%patch35 -p1 -b .tray-icon
%patch41 -p1 -b .default-utf8
%patch50 -p1 -b .active-channel-switch
%patch51 -p1 -b .freenode-ports
%patch52 -p1 -b .libnotify07
%patch53 -p1 -b .link-against-libnotify
%patch54 -p1

sed -i -e 's/#define GTK_DISABLE_DEPRECATED//g' src/fe-gtk/*.c

%build
# Remove CVS files from source dirs so they're not installed into doc dirs.
find . -name CVS -type d | xargs rm -rf

export CFLAGS="$RPM_OPT_FLAGS $(perl -MExtUtils::Embed -e ccopts)"
export LDFLAGS=$(perl -MExtUtils::Embed -e ldopts)

# For xchat-2.8.8-link-against-libnotify.patch
autoconf
autoheader

%configure --disable-textfe \
           --enable-gtkfe \
           --enable-openssl \
           --enable-python \
           --enable-tcl=%{_libdir} \
           --enable-ipv6 \
           --enable-spell=libsexy \
           --enable-shm \
           --enable-ntlm

# gtkspell breaks Input Method commit with ENTER

make %{?_smp_mflags}


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Get rid of libtool archives
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/xchat/plugins/*.la

# Install the .desktop file properly
%{__rm} -f $RPM_BUILD_ROOT%{_datadir}/applications/xchat.desktop
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category=IRCClient \
  --add-category=GTK xchat.desktop

%find_lang %{name}

# do not Provide plugins .so
%define _use_internal_dependency_generator 0
%{__cat} << \EOF > %{name}.prov
#!%{_buildshell}
%{__grep} -v %{_docdir} - | %{__find_provides} $* \
	| %{__sed} '/\.so\(()(64bit)\)\?$/d'
EOF
%define __find_provides %{_builddir}/%{name}-%{version}/%{name}.prov
%{__chmod} +x %{__find_provides}


%post
# Install schema
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule /etc/gconf/schemas/apps_xchat_url_handler.schemas >& /dev/null || :


%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule /etc/gconf/schemas/apps_xchat_url_handler.schemas >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule /etc/gconf/schemas/apps_xchat_url_handler.schemas >& /dev/null || :
fi

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README ChangeLog
%doc plugins/plugin20.html plugins/perl/xchat2-perl.html
%{_bindir}/xchat
%dir %{_libdir}/xchat
%dir %{_libdir}/xchat/plugins
%{_libdir}/xchat/plugins/perl.so
%{_libdir}/xchat/plugins/python.so
%{_datadir}/applications/xchat.desktop
%{_datadir}/pixmaps/*
%{_sysconfdir}/gconf/schemas/apps_xchat_url_handler.schemas
%{_datadir}/dbus-1/services/org.xchat.service.service

%files tcl
%defattr(-,root,root)
%{_libdir}/xchat/plugins/tcl.so

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1:2.8.8-13
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1:2.8.8-12
- 为 Magic 3.0 重建

* Mon Nov 19 2012 Liu Di <liudidi@gmail.com> - 1:2.8.8-11
- 为 Magic 3.0 重建

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:2.8.8-10
- Perl mass rebuild

* Tue Apr  7 2011 Christopher Aillon <caillon@redhat.com> - 1:2.8.8-9
- Link against libnotify (#693362)

* Tue Apr  7 2011 Christopher Aillon <caillon@redhat.com> - 1:2.8.8-8
- Update the dynamic libnotify check for the newer soname (#693362)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.8-6
- Requires: alsa-utils for aplay (#661957)

* Mon Nov 15 2010 Owen Taylor <otaylor@redhat.com> - 1:2.8.8-5
- Add patch to work with libnotify-0.7

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:2.8.8-4
- Rebuild against python 2.7

* Thu Jun 03 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.8-3
- Rebuild again for perl-5.12.0

* Thu Jun 03 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.8-2
- --enable-ntlm (no longer enabled by default)

* Thu Jun 03 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.8-1
- Update to 2.8.8 (#597735)
- Use xz tarball (new in 2.8.8)
- Drop smallfixes, redhat-desktop (remaining part), shm-pixmaps and
  connect-mnemonic patches (all fixed upstream)

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:2.8.6-18
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-17
- Add port numbers for Freenode (Debarshi Ray)

* Fri Apr 09 2010 Rudolf Kastl <rkastl@redhat.com> - 1:2.8.6-16
- Added IRCClient .desktop file subcategory (#485306)
- Added GTK .desktop file subcategory
- Added curly brackets to the name macro for consistency.

* Wed Dec 16 2009 Kevin Fenzi <kevin@tummy.com> - 1:2.8.6-15
- Add patch to allow switching to next channel with activity.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:2.8.6-14
- rebuild against perl 5.10.1

* Thu Sep 10 2009 Christopher Aillon <caillon@redhat.com> - 1:2.8.6-13
- Drop the antiquated OPN reference

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:2.8.6-12
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.8.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-10
- Fixed patch for the "C_onnect" issue (#512034, Edward Sheldrake)

* Thu Jul 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-9
- Fix literal underscore in "C_onnect" button (#512034, Matthias Clasen)

* Mon Jun 29 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-8
- Change Name in xchat.desktop to XChat IRC (#293841)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.8.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-6
- fix filtering of Provides on lib64 architectures

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-5
- rebuild for new OpenSSL

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:2.8.6-4
- Rebuild for Python 2.6

* Mon Aug 11 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-3
- rebuild for fixed redhat-rpm-config (#450271)

* Mon Jul 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-2
- apply xc286-smallfixes.diff from upstream
- don't #define GTK_DISABLE_DEPRECATED (fixes build against current GTK+)

* Sun Jun 15 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.6-1
- update to 2.8.6
- drop upstream patches (already applied in 2.8.6)
- set default charset to UTF-8 (2.8.6 changed it to Latin1)

* Thu May 22 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-16
- fix more bugs in xchat-2.8.4-shm-pixmaps.patch (#282691)

* Tue Apr  1 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-15
- remove --disable-panel which has been ignored since 2.0.0
- add missing BR libntlm-devel (thanks to Karsten Hopp)

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:2.8.4-14
- rebuild for new perl

* Mon Feb 18 2008 Christopher Aillon <caillon@redhat.com> - 1:2.8.4-13
- Rebuild to celebrate my birthday (and GCC 4.3)

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:2.8.4-12
- rebuild for new perl

* Sat Jan 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-11
- fix bug in xchat-2.8.4-shm-pixmaps.patch (Adam Jackson, #429218)

* Thu Jan  3 2008 Christopher Aillon <caillon@redhat.com> 1:2.8.4-10
- Rebuild

* Thu Dec 20 2007 Adam Jackson <ajax@redhat.com> 1:2.8.4-9
- xchat-2.8.4-shm-pixmaps.patch: MIT-SHM pixmaps are optional, and when
  using EXA they are not available.  Check that the server supports them
  before trying to create them so we don't crash.

* Wed Dec 19 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-8
- apply xc284-fix-scrollbfdleak.diff from upstream

* Wed Dec  5 2007 Christopher Aillon <caillon@redhat.com> - 1:2.8.4-7
- Fix the icon key in the .desktop file to validate

* Sat Oct 13 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-6
- drop obsolete xchat-2.4.4-unrealize.patch (fixed upstream for a while)
- drop broken xchat-2.4.3-im_context_filter_keypress.patch (#295331)

* Wed Sep 26 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-5
- apply xc284-improvescrollback.diff from upstream

* Thu Aug 23 2007 Remi Collet <Fedora@FamilleCollet.com> - 1:2.8.4-4.fc8.1
- F-8 rebuild (BuildID)

* Sat Aug 11 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-4
- add missing BR perl(ExtUtils::Embed)

* Fri Aug  3 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-3
- specify GPL version in License tag

* Tue Jul 10 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-2
- apply xc284-scrollbmkdir.diff from upstream

* Wed Jul  4 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.4-1
- update to 2.8.4
- drop xc282-fixtrayzombies.diff (already in 2.8.4)
- rebase redhat-desktop and tray-icon patches

* Fri Jun 22 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-12
- install the .desktop file with --vendor="" to keep the old name

* Thu Jun 21 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-11
- add missing BR desktop-file-utils

* Thu Jun 21 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-10
- remove Application; and X-Red-Hat-Extras; categories from .desktop file
  (merge review #226551)
- install the .desktop file properly (merge review #226551)

* Tue Jun 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-9
- build against system libsexy instead of static sexy-spell-entry now that this
  is possible (Core-Extras merge)

* Sat Jun  2 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-8
- disable tray icon by default (#241923)

* Thu May 31 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-7
- revert to redhat-desktop patch pending further discussion

* Thu May 31 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-6
- apply xc282-fixtrayzombies.diff from upstream

* Wed May 30 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-5
- remove Requires: gtkspell as gtkspell is not currently being used

* Mon May 28 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-4
- set explicit libdir for Tcl so it's found on lib64 arches (Remi Collet)
- move Tcl plugin into subpackage
  (not an incompatible change as this was not built in f7-final at all)

* Mon May 28 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-3
- use versioned Provides/Obsoletes to allow future package split

* Mon May 28 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:2.8.2-2
- merge updates by Remi Collet and Marius Feraru (#224180)
- mention Tcl in description
- add release and user name to buildroot
- follow desktop-entry-spec on Name and GenericName as required by the Packaging
  Guidelines
- drop BR gtkspell-devel as it's not currently used

* Thu Apr  5 2007 Remi Collet <RPMS@FamilleCollet.com> - 1:2.8.2-1.fc6.remi
- update to 2.8.2

* Sat Mar 24 2007 Matthias Clasen <mclasen@redhat.com> - 1:2.6.6-9
- Own /usr/lib/xchat (#166731)

* Thu Jan 25 2007 Marius Feraru <altblue@n0i.net> - 1:2.8.0-1.n0i.1
- version 2.8.0
- disabled some patches: nonblock, locale (fi, es)
- enabled fast tinting
- fixed "exchant" typo
- switched to using the "make install" (DESTDIR works)
- simplified gconf schema disabling method
- dropped plugins mover
- updated "Get rid of static libs"
- dropped xchat-remote
- updated build requirements
- dropped "default-webbrowser" patches (xchat tries to do it better now)
- do not provide "perl.so", "python.so", etc
- own everything under %%{_libdir}/xchat
- converted spec file to UTF8
- fixed desktop entry category (dropping "Application")
- keep plugins documentation

* Tue Jan 16 2007 Remi Collet <RPMS@FamilleCollet.com> - 1:2.8.0-2.fc6.remi
- add Provides/Osboletes for extensions (split RPM available on xchat.org).
- longer description
- enable tcl extension
- Requires gtk >= 2.10.0

* Mon Jan 15 2007 Remi Collet <RPMS@FamilleCollet.com> - 1:2.8.0-1.fc6.remi
- update to 2.8.0
- add upstream patches (xc280-fix-back.diff, xc280-fix-ja.diff)

* Fri Nov  3 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.6.6-8
- Silence %%pre (#213838)

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.6.6-7
- Fix scripts according to packaging guidelines

* Tue Oct 17 2006 Matthias Clasen <mclasen@redhat.com> - 1:2.6.6-6
- Tighten up Requires (#203813)

* Sat Oct  7 2006 David Woodhouse <dwmw2@redhat.com> - 1:2.6.6-5
- Fix nonblocking SSL socket behaviour

* Mon Aug 28 2006 Warren Togami <wtogami@redhat.com> - 1:2.6.6-4
- add upstream 2.6.6 es patch

* Wed Aug 23 2006 Warren Togami <wtogami@redhat.com> - 1:2.6.6-3
- enable optional spell checking if you install enchant
  because gtkspell is currently unusable (#201116)

* Thu Aug 17 2006 Warren Togami <wtogami@redhat.com> - 1:2.6.6-2
- disable gtkspell because it breaks Input Method commit
- apply upstream fi patch

* Wed Aug  2 2006 Marc Deslauriers <marcdeslauriers@videotron.ca> -  1:2.6.6-1
- Update to 2.6.6
- Removed upstreamed dbus patch
- Enabled gtkspell support

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> -  1:2.6.0-6
- Rebuild against dbus

* Mon May 22 2006 Jesse Keating <jkeating@redhat.com> - 1:2.6.0-5
- Adding missing buildreq (bz:191577, thanks Paul F.)

* Sun Feb 12 2006 Christopher Aillon <caillon@redhat.com> - 1:2.6.0-4
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:2.6.0-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 1:2.6.0-3.1
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 1:2.6.0-3
- rebuild for new dbus

* Tue Nov 15 2005 Florian La Roche <laroche@redhat.com> 1:2.6.0-2
- Require(post): GConf2

* Thu Nov 10 2005 Christopher Aillon <caillon@redhat.com> 1:2.6.0-1
- Update to 2.6.0

* Wed Nov  9 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.5-2
- Rebuild against newer openssl

* Mon Sep 19 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.5-1
- X-Chat 2.4.5

* Wed Aug 17 2005 Matthias Clasen <mclasen@redhat.com> 1:2.4.4-3
- Fix a bug that could lead to occasional crashes

* Mon Aug 15 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.4-2
- Rebuild

* Sun Jun 26 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.4-1
- Update to xchat-2.4.4

* Sun May 15 2005 Warren Togami <wtogami@redhat.com> 1:2.4.3-3
- Prevent interception of down arrow during Input Method (#144588 tagoh)

* Thu Apr 14 2005 Warren Togami <wtogami@redhat.com> 1:2.4.3-2
- fix plugins on lib64 (#113188 Ville Skytta)

* Sun Apr 03 2005 Warren Togami <wtogami@redhat.com> 1:2.4.3-1
- 2.4.3, use perl MODULE_COMPAT

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.2-3
- Fix crash when right clicking users whose away msg is unknown.

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.2-2
- Add user's away message to right click menu, if known

* Thu Mar 17 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.2-1
- Update to 2.4.2

* Sat Mar  5 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.1-4
- Rebuild against GCC 4.0

* Tue Jan 18 2005 Chip Turner <cturner@redhat.com> 1:2.4.1-3
- rebuild for new perl

* Tue Jan  4 2005 Christopher Aillon <caillon@redhat.com> 1:2.4.1-2
- Add Dan Reed's CTCP patch to support multiline messages (#136545)

* Tue Nov 23 2004 Christopher Aillon <caillon@redhat.com> 1:2.4.1-1
- Update to 2.4.1

* Mon Sep 20 2004 Daniel Reed <djr@redhat.com> 1:2.4.0-3
- #132967 Remove GenericName

* Tue Aug 17 2004 Daniel Reed <djr@redhat.com> 1:2.4.0-2
- #125846 Change xchat.desktop names to "IRC"

* Sun Aug 15 2004 Christopher Aillon <caillon@redhat.com> 1:2.4.0-1
- Update to 2.4.0
- Fix simplify-to-use-gnome-open and simplify-to-use-htmlview patches
  to not conflict every time upstream modifies the urlhandler list.
- Remove focus and tab completion patches (no longer needed)

* Mon Jul 26 2004 Christopher Aillon <caillon@redhat.com> 1:2.0.10-3
- Update upstream patch to fix tab completion crash
- Add upstream patch to fix focus crash on some window managers.

* Fri Jul  9 2004 Mike A. Harris <mharris@redhat.com> 1:2.0.10-2
- Added upstream xc2010-fixtabcomp.diff patch to fix SEGV in tab completion

* Sat Jul 03 2004 Christopher Aillon <caillon@redhat.com> 1:2.0.10-1
- Update to 2.0.10

* Wed Jun 23 2004 Christopher Aillon <caillon@redhat.com> 1:2.0.9-1
- Update to 2.0.9
- Fixed the URL handler menu patches to apply.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar  9 2004 Mike A. Harris <mharris@redhat.com> 1:2.0.7-5
- Bump and rebuild for Fedora devel, to sync up with new perl
- Remove require_autoconf conditional, and conditionalized autoconf BuildRequires

* Fri Mar  5 2004 Mike A. Harris <mharris@redhat.com> 1:2.0.7-4
- Added xchat-2.0.7-simplify-to-use-gnome-open-for-default-webbrowser.patch
  and xchat-2.0.7-simplify-to-use-htmlview-for-default-webbrowser.patch to
  simplify the default URL handler menu to point only to the default system
  web browser by using gnome-open on Fedora Core 2 and later, or htmlview
  on earlier OS releases.  This is added to improve user friendliness (#82331)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Mike A. Harris <mharris@redhat.com> 1:2.0.7-1.FC1.0
- Rebuild xchat 2.0.7-3 as 2.0.7-1.FC1.0 for release as an enhancement erratum
  for Fedora Core 1.  Also fixes AMD64 64bit issues reported in bug (#114237)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 1:2.0.7-3
- rebuilt

* Mon Jan 26 2004 Jeremy Katz <katzj@redhat.com> 1:2.0.7-2
- rebuild for new perl version

* Sat Jan 10 2004 Mike A. Harris <mharris@redhat.com> 1:2.0.7-1
- Updated to xchat 2.0.7
- Removed already integrated patches, including:  xc204-fixperlui.diff,
  xchat-2.0.4-screen-position-fix.patch, xchat-2.0.4-exec-shield-GNU-stack.patch
- Added a new rpm macro require_autoconf, which is disabled (0) by default, as
  it seems no longer necessary to run autoconf prior to ./configure, so we no
  longer need to BuildRequire autoconf 2.54 either.

* Fri Oct 24 2003 Mike A. Harris <mharris@redhat.com> 2.0.4-4
- Added xchat-2.0.4-exec-shield-GNU-stack.patch from Arjan, to allow xchat to
  be be protected by exec shield if the system has exec-shield enabled.

* Fri Sep 19 2003 Mike A. Harris <mharris@redhat.com> 2.0.4-3.EL
- Rebuilt 2.0.4-3 for Taroon as 2.0.4-3.EL

* Fri Sep 19 2003 Mike A. Harris <mharris@redhat.com> 2.0.4-3
- Added xchat-2.0.4-screen-position-fix.patch to fix problem where xchat
  doesn't remember it's screen location between invocations (#103896)

* Sat Aug 30 2003 Mike A. Harris <mharris@redhat.com> 2.0.4-2
- Updated xchat-2.0.4-redhat-desktop-file.patch

* Thu Aug 28 2003 Mike A. Harris <mharris@redhat.com> 2.0.4-1
- Updated to xchat 2.0.4
- Removed unneeded patches xc203-fixtint.diff, xc203-fix-cps.diff
- Added upstream patch xc204-fixperlui.diff
- Updated autoconf dependancy to version 2.54 and greater as xchat wont
  compile otherwise.  Meaning Red Hat Linux 9 or higher is needed.

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.3-4
- rebuild

* Mon Jul 14 2003 Chip Turner <cturner@redhat.com>
- rebuild for new perl 5.8.1

* Thu Jul 10 2003 Mike A. Harris <mharris@redhat.com> 2.0.3-2
- Added xc203-fix-cps.diff patch from upstream to fix cps calculation
- TCL plugin was getting built even though we don't want it, so now we pass
  --enable-tcl or --disable-tcl explicitly, depending on with_tclplugin macro

* Mon Jun 30 2003 Mike A. Harris <mharris@redhat.com> 2.0.3-1.EL
- Rebuilt 2.0.3-1 as 2.0.3-1.EL for Red Hat Enterprise Linux development

* Mon Jun 30 2003 Mike A. Harris <mharris@redhat.com> 2.0.3-1
- Updated to xchat 2.0.3
- Dropped old patches: xc202-fixdetach.diff, xc202-fixurlg.diff,
  xchat-2.0.2-lib64-cleanup-for-python.patch
- Added upstream patch: xc203-fixtint.diff

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Mike A. Harris <mharris@redhat.com> 2.0.2-7
- Added back BuildRequires autoconf, and call autoconf prior to ./configure
  as it seems to make xchat build successfully.  Have not bothered to figure
  out why calling autoconf is needed.  Something for a rainy day.

* Thu May 29 2003 Mike A. Harris <mharris@redhat.com> 2.0.2-6
- Removed gnome-libs BuildRequires as it is bogus now
- Removed autoconf BuildRequires and usage, as it should be unneeded
- Added new BuildRequires on gettext, bison >= 1.35, glib2-devel >= 2.0.3,
  gtk2-devel >= 2.0.3, /bin/sed  (#91676 - Warren Togami)
- Removed dead patches: xchat-1.8.9-perlcrypt.patch, xchat-1.8.9-korean-fontset.patch

* Wed May 21 2003 Mike A. Harris <mharris@redhat.com> 2.0.2-5
- Removed xchat.desktop file, as it was earlier replacedwith a patch
- Converted xchat-2.0.2-redhat-desktop-file.patch to be UTF-8 clean now,
  instead of the various random legacy mix of encodings it was, updating
  the following: es, ko, uk, zh_TW

* Tue May 20 2003 Mike A. Harris <mharris@redhat.com> 2.0.2-4
- Replace explicit perl package name-epoch-version Requires added in 2.0.2-3
  with a more robust and generic solution of querying perl for the archlibexp
  dir during building, and requiring it instead

* Tue May 20 2003 Bill Nottingham <notting@redhat.com> 2.0.2-3
- rebuild against new (old?) perl, add epoch to dependency

* Sat May 17 2003 Mike A. Harris <mharris@redhat.com> 2.0.2-1
- Updated to new xchat 2.0.2 based on GTK2
- Dropped unneeded patches xchat-1.8.1-konqueror.patch,
  xchat-1.8.4-fix-USE_GNOME.patch
- Updated xchat-2.0.2-freenode.patch to refer to Openprojects.net
- Removed doc/xchat.sgml doc/*.html scripts-python scripts-perl from %%doc
- Added xchat-2.0.2-redhat-desktop-file.patch to patch the supplied xchat
  desktop file, instead of replacing it and trying to stay in sync
- Added xchat-2.0.2-lib64-cleanup-for-python.patch which fixes build problems
  on lib64 archs, and replaces xchat-multilib.patch
- Added with_tclplugin macro and default it to disabled

* Mon Mar 17 2003 Mike A. Harris <mharris@redhat.com> 1.8.11-8
- Added xchat-1.8.11-nickall.patch which was written by Fabio Olive Leite,
  sent to me by Rik van Riel

* Wed Feb 19 2003 Bill Nottingham <notting@redhat.com> 1.8.11-7
- ship single desktop in %{_datadir}/applications, not /etc/X11/applnk

* Fri Jan 31 2003 Mike A. Harris <mharris@redhat.com> 1.8.11-6
- Added xchat-1.8.11-freenode.patch to rename all openprojects.net entries
  to freenode.net in the default server list.  Patch courtesy of Dan Burcaw
  from bug (#81704)

* Wed Jan 22 2003 Mike A. Harris <mharris@redhat.com> 1.8.11-5
- Removed double .desktop file (#81874,82315)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.8.11-4
- rebuilt

* Tue Jan  7 2003 Mike A. Harris <mharris@redhat.com> 1.8.11-3
- Add bugfix from xchat.org xc1811fixststint.diff

* Tue Jan  7 2003 Mike A. Harris <mharris@redhat.com> 1.8.11-2
- Remove CVS files from source dirs so they're not installed into doc dirs.

* Tue Jan  7 2003 Mike A. Harris <mharris@redhat.com> 1.8.11-1
- Update to xchat 1.8.11 bugfix release, fixes various runtime crashes
- Remove now included patches: xchat-1.8.10-urlhandler-open-in-new-tab.patch,
  xchat-1.8.10-beep-beep-beep.patch

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.10-13
- Pick up OpenSSL configuration from pkgconfig, if available
- Add openssl-devel and pkgconfig as buildreqs

* Wed Dec 11 2002 Elliot Lee <sopwith@redhat.com> 1.8.10-12
- Fix broken libpython path on multilibbed systems (patch13)
- _smp_mflags

* Tue Nov 26 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-11
- Added xchat-1.8.10-urlhandler-open-in-new-tab.patch to offer the option of
  opening a URL in a new tab of an existing browser window rather than a new
  window

* Sat Nov 23 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-10
- Added BuildRequires: python-devel to hopefully pick up a missing dep
  causing package build failure in timp's nightly builds.
- Removed dead patches
- Updated package summary and description to be more user friendly by
  rewording, and removing scary words like GNOME, GTK and other irrelevance

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-9
- Made sure {_sysconfdir}/X11/applnk/Internet/xchat.desktop gets packaged
- Removed some conditional weirdness in %%files list.  This may break xchat
  erratum releases on Red Hat Linux 7.x.  May need to be fixed in future.

* Fri Aug 23 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-7
- Added Requires line so that xchat requires the exact version of perl
  be installed, that was used to compile it, since the embedded perl
  interpreter will break, if you upgrade perl

* Thu Aug 15 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-6
- Fix Bill's beep beep beep bug (#71651)

* Wed Aug 14 2002 Jonathan Blandford <jrb@redhat.com> 1.8.10-5
- actually install the desktop file.

* Fri Aug  9 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-3
- Added http://xchat.org/files/source/1.8/patches/xc1810fixme.diff to fix
  bug with using /ME in a /QUERY window.  (#71179)

* Wed Aug  7 2002 Mike A. Harris <mharris@redhat.com> 1.8.10-2
- Updated to xchat 1.8.10 to fix a few bugs where a remote ircd could cause
  the xchat client to crash.  This is a bugfix only release.

* Tue Aug  6 2002 Mike A. Harris <mharris@redhat.com> 1.8.9-10
- Added Korean fontset support to fix bug (#69771)

* Mon Aug  5 2002 Mike A. Harris <mharris@redhat.com> 1.8.9-9
- Enabled python scripting which was somehow disabled somewhere along the
  line by default in upstream sources, and we missed catching it. (#70816)

* Sun Aug  4 2002 Mike A. Harris <mharris@redhat.com> 1.8.9-8
- Created new-style net-xchat.desktop file (#69541)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.8.9-7
- automated rebuild

* Tue Jun 18 2002 Mike A. Harris <mharris@redhat.com> 1.8.9-6
- updated the package description
- Added CFLAGS and LDFLAGS export vars before configure to fix rpath problem

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Mike A. Harris <mharris@redhat.com> 1.8.9-2
- Updated to xchat 1.8.9

* Mon Apr  8 2002 Mike A. Harris <mharris@redhat.com> 1.8.8-5
- Re-enabled GNOME support due to user complaints of pixmaps missing, key
  bindings, and other fairly important features no longer working.

* Tue Mar 27 2002 Mike A. Harris <mharris@redhat.com> 1.8.8-4
- Disabled GNOME support since it doesn't seem too useful anyways, and forces
  all xchat users to install GNOME libs even if they use KDE. (#59626)
- Updated URL and source lines in spec.

* Wed Mar  6 2002 Mike A. Harris <mharris@redhat.com> 1.8.8-1
- Updated to xchat 1.8.8

* Tue Feb 26 2002 Mike A. Harris <mharris@redhat.com> 1.8.7-6
- Built in new buildroot

* Tue Feb  5 2002 Mike A. Harris <mharris@redhat.com> 1.8.7-5
- Added xchat-1.8.7-use-sysconf-to-detect-cpus.patch to use glibc's sysconf()
  to detect the number of processors available.

* Mon Feb  4 2002 Mike A. Harris <mharris@redhat.com> 1.8.7-4
- Enabled IPv6 support as per the request for enhancement (#52124)

* Thu Jan 24 2002 Mike A. Harris <mharris@redhat.com> 1.8.7-3
- Rebuilt in new build environment

* Thu Jan 10 2002 Mike A. Harris <mharris@redhat.com> 1.8.7-2
- Updated to xchat 1.8.7
- New release fixes security vulnerability in CTCP reply
- Built erratum for all supported releases (1.8.7-1.62.0, 1.8.7-1.70.0,
  1.8.7-1.71.0, 1.8.7-1.72.0)
- Removed konqueror patch as it is integrated now.

* Sat Jan  5 2002 Mike A. Harris <mharris@redhat.com> 1.8.6-2
- Enabled ssl support with --enable-openssl
- Also built releases 1.72.0, 1.71.0, 1.70.0, 1.62.0 for erratum release

* Mon Dec 10 2001 Mike A. Harris <mharris@redhat.com> 1.8.6-1
- Updated to xchat 1.8.6

* Tue Nov 13 2001 Mike A. Harris <mharris@redhat.com> 1.8.5-1
- Updated to xchat 1.8.5
- Added f to rm -r in install and clean sections

* Sun Oct  7 2001 Mike A. Harris <mharris@redhat.com> 1.8.4-1
- Updated to 1.8.4, now using tar.bz2
- Removed kanjiconv-fix patch as it is integrated now
- Added xchat-1.8.4-fix-USE_GNOME.patch to fix simple ifdef USE_GNOME typo

* Fri Jul 13 2001 Akira TAGOH <tagoh@redhat.com> 1.8.1-2
- fixed check locale.
- don't save kanji_conv.
  always check locale. however anyone can change the option from
  the settings menu.

* Thu Jul 12 2001 Havoc Pennington <hp@redhat.com>
- upgrade to 1.8.1
- remove autoconnect patch since it's upstream
- remove japanese patch, upstream seems to have applied
  parts of it and changelog says there's upstream support.
  (this patch was pretty huge to maintain in an SRPM anyway...)
- put scripts-python scripts-perl in docs bug #28521
- remove patch to include locale.h, gone upstream
- upgrade konqueror patch

* Thu Jul 12 2001 Havoc Pennington <hp@redhat.com>
- nevermind, BuildRequires gnome-libs, that should 
  close #48923

* Thu Jul 12 2001 Havoc Pennington <hp@redhat.com>
- fix file list to not include absolute path "/usr/share/..."
  no idea how that ever worked at all. closes #48923

* Mon Jun 25 2001 Karsten Hopp <karsten@redhat.de>
- use konqueror, not kfmclient on URLs

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify
- use %%{_tmppath}
- make it compile

* Tue Feb 13 2001 Akira TAGOH <tagoh@redhat.com>
- Added Japanese patch.

* Tue Feb 13 2001 Havoc Pennington <hp@redhat.com>
- patch that may fix autoconnections (bug 27093)

* Mon Jan 22 2001 Havoc Pennington <hp@redhat.com>
- 1.6.3
- remove patch to desktop file (Internet->Application), seems to 
  have gone upstream

* Sat Dec 9 2000 Havoc Pennington <hp@redhat.com>
- Remove security fix which has been merged upstream
- upgrade to 1.6.1

* Sat Aug 19 2000 Havoc Pennington <hp@redhat.com>
- Don't use /bin/sh to interpret URLs from the net

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Updated Epoch

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Havoc Pennington <hp@redhat.com>
- Install HTML docs

* Fri Jun 16 2000 Preston Brown <pbrown@redhat.com>
- fix desktop entry

* Fri May 19 2000 Havoc Pennington <hp@redhat.com>
- rebuild for the Winston tree, update to 1.4.2
