Summary:	The GIMP ToolKit
Name:		gtk+
Epoch:		1
Version:	1.2.10
Release:	72%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		http://www.gtk.org/
Source0:	ftp://ftp.gimp.org/pub/gtk/v1.2/gtk+-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	gtk1 = %{version}-%{release}

Source1:	gtkrc-default
Source2:	gtk+-pofiles.tar.gz
Source3:	gtkrc.ja.utf8
Source4:	gtkrc.ko.utf8
Source5:	gtkrc.zh_CN.utf8
Source6:	gtkrc.zh_TW.utf8

Patch1:		gtk+-1.2.10-ahiguti.patch
Patch5:		gtk+-1.2.8-wrap-alnum.patch
# Suppress alignment warnings on ia64
Patch10:	gtk+-1.2.10-alignment.patch
# Improve exposure compression
Patch11:	gtk+-1.2.10-expose.patch
# Handle focus tracking for embedded window properly
Patch12:	gtk+-1.2.10-focus.patch
# Find gtkrc files for the current encoding better
Patch13:	gtk+-1.2.10-encoding.patch
# Don't screw up CTEXT encoding for UTF-8
Patch14:	gtk+-1.2.10-ctext.patch
# Don't warn about missing fonts for UTF-8
Patch15:	gtk+-1.2.10-utf8fontset.patch
# Accept KP_Enter as a synonym for Return everywhere
Patch16:	gtk+-1.2.10-kpenter.patch
# Allow theme switching to work properly when no windows are realized
Patch17:	gtk+-1.2.10-themeswitch.patch
# Fix crash when switching themes
Patch18:	gtk+-1.2.10-pixmapref.patch
# Fix computation of width of missing characters
Patch19:	gtk+-1.2.10-missingchar.patch
# Fix sizes of Ukrainian fontsets
Patch20:	gtk+-1.2.10-ukfont.patch
# Fix file selection delete-dir when changing directory problem
# also, fix memory corruption problem when changing directories.
Patch21:	gtk+-1.2.10-deletedir.patch
# Improve warning for missing fonts
Patch22:	gtk+-1.2.10-fontwarning.patch
# Allow themes to make scrollbar trough always repaint
Patch23:	gtk+-1.2.10-troughpaint.patch
# Fix a crash that can happen in some apps when the current
# locale is not supported by XLib.
Patch24:	gtk+-1.2.10-localecrash.patch
# Patch from CVS to fix b.g.o #56349
Patch26:	gtk+-1.2.10-dndorder.patch
# Patch from CVS to fix b.g.o #94812
Patch27:	gtk+-1.2.10-clistfocusrow.patch
# Fix GTK+ to obey X server's default bell volume
Patch28:	gtk+-1.2.10-bellvolume.patch
# Hack up the configure scripts to deal with some obscure
# breakage with ancient libtool
Patch29:	gtk+-1.2.10-libtool.patch
# Add a dependency on libgdk to libgtk (#106677)
Patch30:	gtk+-1.2.10-gtkgdkdep.patch
Patch31:	gtk+-underquoted.patch
Patch32:	gtk+-1.2.10-ppc64.patch
# do not allow for undefined symbols in shared libraries -- Rex
Patch33:	gtk+-1.2.10-no_undefined.patch
# http://bugzilla.redhat.com/222298
Patch34:	gtk+-1.2.10-multilib.patch
# Remove redundant shared library dependencies
Patch35:	gtk+-1.2.10-unused-deps.patch

BuildRequires:	glib-devel >= 1:%{version}
BuildRequires:	automake14 autoconf213
BuildRequires:	libtool
BuildRequires:	gettext
%if 0%{?fedora} > 4 || 0%{?rhel} > 4
%global x_deps	libX11-devel libXext-devel libXi-devel libXt-devel
%else
%global x_deps	xorg-x11-devel
## This can be used for legacy too -- Rex
#global	x_deps	XFree86-devel
%endif
BuildRequires:	%{x_deps} 

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for
creating graphical user interfaces for the X Window System. GTK+ was
originally written for the GIMP (GNU Image Manipulation Program) image
processing program, but is now used by several other programs as
well.

%package	devel
Summary:	Development tools for GTK+ (GIMP ToolKit) applications
Group:		Development/Libraries
Provides:	gtk1-devel = %{version}-%{release}
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	glib-devel
Requires:	pkgconfig
Requires:	%{x_deps} 
## info files not included
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description devel
Libraries, header files and documentation for developing GTK+ 
(GIMP ToolKit) applications.


%prep
%setup -q -a 2

%patch1 -p1 -b .ahiguti
%patch5 -p1 -b .alnum
%patch10 -p1 -b .alignment
%patch11 -p1 -b .expose
%patch12 -p1 -b .focus
%patch13 -p1 -b .encoding
%patch14 -p1 -b .ctext
%patch15 -p1 -b .utf8fontset
%patch16 -p1 -b .kpenter
%patch17 -p1 -b .themeswitch
%patch18 -p1 -b .pixmapref
%patch19 -p1 -b .missingchar
%patch20 -p1 -b .ukfont
%patch21 -p1 -b .deletedir
%patch22 -p1 -b .fontwarning
%patch23 -p0 -b .troughpaint
%patch24 -p1 -b .localecrash
%patch26 -p0 -b .dndorder
%patch27 -p0 -b .clistfocusrow
%patch28 -p1 -b .bellvolume
%patch29 -p1 -b .libtool
%patch30 -p1 -b .gtkgdkdep
%patch31 -p1 -b .underquoted
%patch32 -p1 -b .ppc64
%patch33 -p1 -b .no_undefined
%patch34 -p1 -b .multilib
%patch35 -p1 -b .unused-deps

# The original config.{guess,sub} do not work on x86_64
#
# The following /usr/lib cannot be %%_libdir !!
%{__cp} -p /usr/lib/rpm/config.{guess,sub} .

#%{__cp} -f %{_datadir}/aclocal/libtool.m4 .
#/usr/bin/libtoolize --copy --force
/usr/bin/automake-1.4
#/usr/bin/aclocal-1.4
/usr/bin/autoconf-2.13
/usr/bin/autoheader-2.13

# Recode docs as UTF-8
for doc in ChangeLog examples/calendar/calendar.c; do
	/usr/bin/iconv -f iso-8859-1 -t utf-8 < ${doc} > ${doc}.utf8
	%{__mv} ${doc}.utf8 ${doc}
done

%build
LIBTOOL=%{_bindir}/libtool \
%configure \
	--disable-static \
	--with-xinput=xfree \
	--with-native-locale

%{__make} %{?_smp_mflags} LIBTOOL=%{_bindir}/libtool


%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot} LIBTOOL=%{_bindir}/libtool INSTALL="%{__install} -p"

#
# Make cleaned-up versions of examples and tutorial for installation
#
./mkinstalldirs tmpdocs/tutorial
%{__install} -p -m0644 docs/html/gtk_tut.html docs/html/gtk_tut-[0-9]*.html docs/html/*.gif tmpdocs/tutorial
for dir in examples/*; do
	if [ -d $dir ]; then
		./mkinstalldirs tmpdocs/$dir
		for file in $dir/* ; do
			case $file in
			*pre1.2.7)
				;;
			*)
				%{__install} -p -m0644 $file tmpdocs/$dir
				;;
			esac
		done
	fi
done

%{__install} -p -m644 -D %{SOURCE1} %{buildroot}/etc/gtk/gtkrc

# Install some extra gtkrc files to improve functioning of GTK+
# in UTF-8 locales for Chinese, Japanese, Korean.
for i in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
	%{__install} -p -m0644 $i %{buildroot}/etc/gtk/
done

# We don't ship the info files
%{__rm} -rf %{buildroot}%{_infodir}

# .la fies... die die die.
%{__rm} -rf %{buildroot}%{_libdir}/lib*.la
# despite use of --disable-static, delete static libs that get built anyway
%{__rm} -rf %{buildroot}%{_libdir}/lib*.a

%find_lang %{name}


%check
%{__make} check LIBTOOL=%{_bindir}/libtool


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/libgdk-1.2.so.*
%{_libdir}/libgtk-1.2.so.*
%{_datadir}/themes/Default/
%dir %{_sysconfdir}/gtk/
%config(noreplace) %{_sysconfdir}/gtk/gtkrc*

%files devel
%defattr(-,root,root,-)
%doc tmpdocs/tutorial/
%doc tmpdocs/examples/
%{_bindir}/gtk-config
%{_includedir}/gtk-1.2/
%{_libdir}/libgdk.so
%{_libdir}/libgtk.so
%{_libdir}/pkgconfig/gdk.pc
%{_libdir}/pkgconfig/gtk+.pc
%{_datadir}/aclocal/gtk.m4
%{_mandir}/man1/gtk-config.1*


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1:1.2.10-72
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 10 2009 Paul Howarth <paul@city-fan.org> 1:1.2.10-70
- don't own dir %%{_datadir}/themes/ (owned by filesystem since F-8, #534097)
- make %%files lists more specific

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.2.10-69
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Paul Howarth <paul@city-fan.org> 1:1.2.10-68
- remove unused shared library dependencies
- use install -p to maintain timestamps where reasonable
- recode docs as UTF-8
- cosmetic spec changes

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1:1.2.10-67
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  2 2008 Patrice Dumas <pertusus@free.fr> 1:1.2.10-66
- rebase the ahiguti patch

* Thu Oct  2 2008 Patrice Dumas <pertusus@free.fr> 1:1.2.10-65
- remove x_ldflags from gtk-config (#462650)

* Wed Oct  1 2008 Patrice Dumas <pertusus@free.fr> 1:1.2.10-64
- copy config.* from rpm directory, those shipped with gtk+ are too old

* Wed Oct 01 2008 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.10-63
- patch_fuzz, fix build (#465033)

* Mon Mar 10 2008 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.10-62
- Provides: gtk1(-devel)

* Mon Feb 18 2008 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.10-61
- fix multilib patch (#341401)

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.10-60 
- respin (gcc43)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-59
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-58
- License: LGPLv2+

* Thu Jan 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-57
- revert libtool-related breakage 

* Thu Jan 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:1.2.10-56
- multilib patch (#222298)
- cleanup auto*/libtool foo 
- drop old/deprecated bits

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-55
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-54
- fc6 respin

* Thu Jun 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-53
- respin, see if still buildable with new mock config (bug #193397)

* Mon Apr 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-52
- install -m644 gtkrc ...
- utf-8 specfile
- comment %%fedora > 4 constructs
- own %%_datadir/themes
- move %%check after %%install

* Sat Apr 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1:1.2.10-51
- cleanup for Extras
- drop Obsoletes: gtk (that must be *way* old)
- drop gdk-pixbuf debpendancy
- fix/re-enable gdkgtkdep patch
- no_undefined patch

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 1:1.2.10-50
- BuildRequires: libXt-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.10-49.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.10-49.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 1:1.2.10-49
- Remove references to obsolete X11R6 paths

* Wed Nov 16 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-48
- Fix Requires of -devel

* Mon Nov  7 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-47
- Remove .la files and static libs

* Tue Nov  7 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-46
- Rebuilt

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-45
- Switch requires to modular X

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-35
- Rebuild with gcc4

* Thu Feb 17 2005 Matthias Clasen <mclasen@redhat.com> 1:1.2.10-34
- Replace Copyright tag in header.

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-33
- Fixed underquoted m4 definition.

* Thu Jun 24 2004 Matthias Clasen <mclasen@redhat.com>
- add missing buildrequires (#124159)

* Tue Jun 16 2004 Matthias Clasen <mclasen@redhat.com>
- rebuilt for RHEL3 U3

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Oct 27 2003 Owen Taylor <otaylor@redhat.com> 1:1.2.10-28.1
- Cave like a cheap house of cards and add gdk-pixbuf dependency (#105613)
- Add gtkrc.*.utf8 RC files for CJK (#84593)
- Add a dependency on libgdk to libgtk (#106677)

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:1.2.10-27.1
- build for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 1.2.10-26
- Run libtoolize/auto* to get an updated libtool that recognizes ppc64

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Owen Taylor <otaylor@redhat.com> 1.2.10-24
- Add a couple of patches from GNOME CVS, fixing a crash
  with CList focus row tracking, and a place where DND
  would get confused.
- Obey the system bell volume (#74802)
- Ship the pkg-config files

* Mon Nov  4 2002 Tim Waugh <twaugh@redhat.com> 1.2.10-23
- Don't install files not shipped.
- Fix gtk-config output for multilib archs.

* Thu Aug 22 2002 Owen Taylor <otaylor@redhat.com>
- Fix a crash that can happen in some apps when the current
  locale is not supported by XLib. (#72157)

* Fri Jul 26 2002 Owen Taylor <otaylor@redhat.com>
- Fix a small memory leak in the .encoding patch (Kjartan Maraas)

* Fri Jul 19 2002 Alexander Larsson <alexl@redhat.com>
- Add troughpaint patch

* Thu Jun 27 2002 Owen Taylor <otaylor@redhat.com>
- Fix UTF-8 font specification not to pick up *-c-* fonts

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Alex Larsson <alexl@redhat.com>
- Require automake 1.4

* Wed Apr 17 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem with incorrect directory contents when changing directories (#63726)

* Mon Apr 15 2002 Havoc Pennington <hp@redhat.com>
- merge translations

* Fri Apr 12 2002 Owen Taylor <otaylor@redhat.com>
- Fix filesel delete-filename-on-dir-change problem
- Improve warning for missing fontset elements

* Thu Apr 11 2002 Owen Taylor <otaylor@redhat.com>
- Fix ukrainian font sizes, minor tweak to russian fonts (#63135)
- Own /etc/gtk/ as well as the files in it (#63139)

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Mon Aug 13 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem with width computation for missing characters

* Sun Aug 12 2001 Owen Taylor <otaylor@redhat.com>
- Fix refcounting problem in gtk_style_copy() that might affect 
  theme switching. (#51580)

* Wed Aug  8 2001 Owen Taylor <otaylor@redhat.com>
- Add fix for theme switching in nautilus sidebar tabs 
  (and other similar situations)

* Sat Jul 21 2001 Owen Taylor <otaylor@redhat.com>
- Accept KP_Enter as well as Return (#21111)

* Wed Jul 11 2001 Owen Taylor <otaylor@redhat.com>
- Further improve exposure compression code

* Tue Jul 10 2001 Owen Taylor <otaylor@redhat.com>
- Omit warnings about character sets not found in fontset,
  if current locale is UTF-8 based. (Hack!)

* Tue Jul  3 2001 Owen Taylor <otaylor@redhat.com>
- Add patch for alignment warnings on ia64
- Add from Alex to vastly improve expose compression
- Add patch to fix focus tracking for embedded windows
- Add patch by Pablo Saratxaga to improve encoding handling 
- Add patch to not screw up CTEXT for UTF-8 locales

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- Upped to version 1.2.10

* Thu Mar 15 2001 Havoc Pennington <hp@redhat.com>
- translations

* Fri Mar  9 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem with focus and no window manager running
- Fix freeing NULL event when copying without a current event

* Mon Mar  5 2001 Trond Eivind Glomsrod <teg@redhat.com>
- langify

* Mon Mar 05 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9
- Patch to fix problem with menus not popping down

* Thu Mar 01 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9pre4

* Wed Feb 28 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9pre3

* Thu Feb 15 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.2.9pre1

* Sat Feb 10 2001 Owen Taylor <otaylor@redhat.com>
- Fix stupid mistake in last version of patch

* Sat Feb 10 2001 Owen Taylor <otaylor@redhat.com>
- New version of theme patch.

* Wed Jan 24 2001 Matt Wilson <msw@redhat.com>
- Japanese ideographs now show up in iswalnum, don't include it in
  the ideograph check (Patch5: gtk+-1.2.8-wrap-alnum.patch)

* Tue Nov 21 2000 Owen Taylor <otaylor@redhat.com>
- Add patch for enabling better themes

* Thu Oct 19 2000 Elliot Lee <sopwith@redhat.com>
- Fix bug in shm patch error handling.

* Fri Aug 18 2000 Jakub Jelinek <jakub@redhat.com>
- fix GtkClist bug

* Sat Aug 12 2000 Owen Taylor <otaylor@redhat.com>
- Add patch to reduce shm segment usage from 6 to 1

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Wed Jul 19 2000 Owen Taylor <otaylor@redhat.com>
- Add BuildPreReq on glib = %%{version}

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun  9 2000 Matt Wilson <msw@redhat.com>
- rebuilt with corrected compiler to fix ABI breakage
- FHS packaging.

* Thu May 25 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.2.8

* Fri May 12 2000 Matt Wilson <msw@redhat.com>
- reapply gtkrc fixes for various locales

* Mon May  1 2000 Matt Wilson <msw@redhat.com>
- build package version 1.2.7

* Mon Feb 21 2000 Owen Taylor <otaylor@redhat.com>
- Fix weird excess " problem that somehow turned up in /etc/gtkrc.LANG

* Mon Feb 14 2000 Owen Taylor <otaylor@redhat.com>
- More patches from 1.2.7

* Fri Feb 04 2000 Owen Taylor <otaylor@redhat.com>
- Set the charset explicitely for the default font to avoid
  problems with XFree86-4.0 where the default charset is
  iso10646-1, not iso8859-1.
- Fix problems with size requisitions for scrolled windows
  that was causing looping. (RH bug #7997)

* Thu Feb 03 2000 Owen Taylor <otaylor@redhat.com>
- Explicitely set the foreground of the tooltips to black
  to avoid bad interactions with themes that set a
  light foreground color.

* Thu Feb 03 2000 Owen Taylor <otaylor@redhat.com>
- Added large patch of bugfixes in stable branch of CVS

* Tue Oct 12 1999 Owen Taylor <otaylor@redhat.com>
- Added Akira Higuti's patch for line-wrapping in GTK+

* Thu Oct 7  1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.6

* Thu Sep 23 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.5
- install tutorial GIFs

* Wed Sep 22  1999 Owen Taylor <otaylor@redhat.com>
- Upgrade to real 1.2.5pre2
- Changed name so upgrade to 1.2.5 will work :-(
- Add extra gtkrc files
- Add examples and English language tutorial to -devel package

* Fri Sep 17 1999 Owen Taylor <otaylor@redhat.com>
- Upgraded to 1.2.5pre2. (Actually, pre-pre-2)

* Tue Aug 17 1999 Michael Fulbright <drmike@redhat.com>
- added threaded patch

* Mon Jun 7 1999 Owen Taylor <otaylor@redhat.com>
- Update for GTK+-1.2.3
- Patches that will be in GTK+-1.2.4
- Patch to keep GTK+ from coredumping on X IO errors
- Patch to improve compatilibity with GTK-1.2.1 (allow
  event mask to be set on realized widgets)

* Mon Apr 19 1999 Michael Fulbright <drmike@redhat.com>
- fixes memory leak

* Mon Apr 12 1999 Owen Taylor <otaylor@redhat.com>
- The important bug fixes that will be in GTK+-1.2.2

* Thu Apr 01 1999 Michael Fulbright <drmike@redhat.com>
- patches from owen to handle various gdk bugs

* Sun Mar 28 1999 Michael Fulbright <drmike@redhat.com>
- added XFree86-devel requirement for gtk+-devel

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.1

* Wed Mar 17 1999 Michael Fulbright <drmike@redhat.com>
- removed /usr/info/dir.gz file from package

* Fri Feb 26 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.2.0

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.0pre2, patched to use --sysconfdir=/etc

* Mon Feb 15 1999 Michael Fulbright <drmike@redhat.com>
- patched in Owen's patch to fix Metal theme

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- bumped up to 1.1.15

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- bumped up to 1.1.14

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- bumped up to 1.1.13

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- bumped up to 1.1.12

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- added Theme directory to file list
- up to 1.1.7 for GNOME freeze

* Sun Oct 25 1998 Shawn T. Amundson <amundson@gtk.org>
- Fixed Source: to point to v1.1 

* Tue Aug 04 1998 Michael Fulbright <msf@redhat.com>
- change %%postun to %%preun

* Mon Jun 27 1998 Shawn T. Amundson
- Changed version to 1.1.0

* Thu Jun 11 1998 Dick Porter <dick@cymru.net>
- Removed glib, since it is its own module now

* Mon Apr 13 1998 Marc Ewing <marc@redhat.com>
- Split out glib package

* Tue Apr  8 1998 Shawn T. Amundson <amundson@gtk.org>
- Changed version to 1.0.0

* Tue Apr  7 1998 Owen Taylor <otaylor@gtk.org>
- Changed version to 0.99.10

* Thu Mar 19 1998 Shawn T. Amundson <amundson@gimp.org>
- Changed version to 0.99.9
- Changed gtk home page to www.gtk.org

* Thu Mar 19 1998 Shawn T. Amundson <amundson@gimp.org>
- Changed version to 0.99.8

* Sun Mar 15 1998 Marc Ewing <marc@redhat.com>
- Added aclocal and bin stuff to file list.
- Added -k to the SMP make line.
- Added lib/glib to file list.

* Fri Mar 14 1998 Shawn T. Amundson <amundson@gimp.org>
- Changed version to 0.99.7

* Fri Mar 14 1998 Shawn T. Amundson <amundson@gimp.org>
- Updated ftp url and changed version to 0.99.6

* Thu Mar 12 1998 Marc Ewing <marc@redhat.com>
- Reworked to integrate into gtk+ source tree
- Truncated ChangeLog.  Previous Authors:
  Trond Eivind Glomsrod <teg@pvv.ntnu.no>
  Michael K. Johnson <johnsonm@redhat.com>
  Otto Hammersmith <otto@redhat.com>
  
