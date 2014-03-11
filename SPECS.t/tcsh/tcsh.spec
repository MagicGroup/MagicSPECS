Summary: An enhanced version of csh, the C shell
Name: tcsh
Version: 6.17
Release: 18%{?dist}
License: BSD
Group: System Environment/Shells
Source: ftp://ftp.astron.com/pub/tcsh/%{name}-%{version}.00.tar.gz
Patch1: tcsh-6.15.00-closem.patch
Patch2: tcsh-6.14.00-tinfo.patch
Patch3: tcsh-6.14.00-unprintable.patch
Patch4: tcsh-6.15.00-hist-sub.patch
Patch6: tcsh-6.15.00-ca-color.patch
Patch7: tcsh-6.14.00-set.patch
Patch8: tcsh-6.14.00-syntax.patch
Patch9: tcsh-6.13.00-memoryuse.patch
Patch11: tcsh-6.14.00-order.patch
Patch12: tcsh-6.15.00-rs-color.patch
Patch13: tcsh-6.17.00-mh-color.patch
# The idea is good, but the patch must be rewritten to be accepted by upstream
# (see tcsh mailing list for more information):
Patch14: tcsh-6.17.00-glob-automount.patch
# Accepted by upstream:
Patch15: tcsh-6.17.00-history.patch
# Accepted by upstream:
Patch16: tcsh-6.17.00-printexitvalue.patch
Patch17: tcsh-6.17.00-testsuite.patch
# Accepted by upstream:
Patch18: tcsh-6.17.00-extrafork.patch
# Accepted by upstream (tcsh-6.17.03b http://bugs.gw.com/view.php?id=109):
Patch19: tcsh-6.17.00-wait-intr.patch
# Accepted by upstream (tcsh-6.17.03b http://bugs.gw.com/view.php?id=112):
Patch21: tcsh-6.17.00-dont-set-empty-remotehost.patch
# Patch by upstream (tcsh-6.17.01b http://mx.gw.com/pipermail/tcsh-bugs/2010-May/000673.html):
Patch22: tcsh-6.17.00-dont-print-history-on-verbose.patch
# Accepted by upstream (tcsh-6.17.03b http://bugs.gw.com/view.php?id=113):
Patch23: tcsh-6.17.00-variable-names.patch
# Accepted by upstream (tcsh-6.17.05b http://mx.gw.com/pipermail/tcsh-bugs/2011-March/000727.html):
Patch24: tcsh-6.17.00-avoid-infinite-loop-pendjob-xprintf.patch
Provides: csh = %{version}
Requires(post): grep
Requires(postun): coreutils, grep
URL: http://www.tcsh.org/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, ncurses-devel, gettext-devel

Provides: /bin/csh, /bin/tcsh

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%setup -q -n %{name}-%{version}.00
%patch1 -p1 -b .closem
%patch2 -p1 -b .tinfo
%patch3 -p1 -b .unprintable
%patch4 -p1 -b .hist-sub
%patch6 -p1 -b .ca-color
%patch7 -p1 -b .set
%patch8 -p1 -b .syntax
%patch9 -p1 -b .memoryuse
%patch11 -p1 -b .order
%patch12 -p1 -b .rs-color
%patch13 -p1 -b .mh-color
%patch14 -p1 -b .glob-automount
%patch15 -p1 -b .history
%patch16 -p1 -b .printexitvalue
%patch17 -p1 -b .testsuite
%patch18 -p1 -b .extrafork
%patch19 -p1 -b .wait-intr
%patch21 -p1 -b .dont-set-empty-remotehost
%patch22 -p1 -b .dont-print-history-on-verbose
%patch23 -p1 -b .variable-names
%patch24 -p1 -b .avoid-infinite-loop-pendjob-xprintf

for i in Fixes WishList; do
 iconv -f iso-8859-1 -t utf-8 "$i" > "${i}_" && \
 touch -r "$i" "${i}_" && \
 mv "${i}_" "$i"
done

%build
# For tcsh-6.14.00-tinfo.patch
autoreconf
%configure --without-hesiod
make %{?_smp_mflags} all
make %{?_smp_mflags} -C nls catalogs

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_bindir}
install -p -m 755 tcsh ${RPM_BUILD_ROOT}%{_bindir}/tcsh
install -p -m 644 tcsh.man ${RPM_BUILD_ROOT}%{_mandir}/man1/tcsh.1
ln -sf tcsh ${RPM_BUILD_ROOT}%{_bindir}/csh
ln -sf tcsh.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/csh.1

magic_rpm_clean.sh

while read lang language ; do
	dest=${RPM_BUILD_ROOT}%{_datadir}/locale/$lang/LC_MESSAGES
	if test -f tcsh.$language.cat ; then
		mkdir -p $dest
		install -p -m 644 tcsh.$language.cat $dest/tcsh
		echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/tcsh"
	fi
done > tcsh.lang << _EOF
en C
_EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
 echo "%{_bindir}/tcsh" >> /etc/shells
 echo "%{_bindir}/csh"	>> /etc/shells
else
 grep -q '^%{_bindir}/tcsh$' /etc/shells || \
 echo "%{_bindir}/tcsh" >> /etc/shells
 grep -q '^%{_bindir}/csh$'  /etc/shells || \
 echo "%{_bindir}/csh"	>> /etc/shells
fi

%postun
if [ ! -x %{_bindir}/tcsh ]; then
 grep -v '^%{_bindir}/tcsh$'  /etc/shells | \
 grep -v '^%{_bindir}/csh$' > /etc/shells.rpm && \
 mv /etc/shells.rpm /etc/shells
fi

%files -f tcsh.lang
%defattr(-,root,root,-)
%doc BUGS FAQ Fixes NewThings WishList complete.tcsh README
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/man1/*.1*

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 6.17-18
- 为 Magic 3.0 重建

* Sun Apr 22 2012 Liu Di <liudidi@gmail.com> - 6.17-17
- 为 Magic 3.0 重建

* Mon Feb 13 2012 Liu Di <liudidi@gmail.com> - 6.17-16
- 为 Magic 3.0 重建

* Thu Mar 24 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-15
- Avoid infinite loop pendjob()-xprintf() when stdout is closed
  Resolves: #690356

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-13
- Modify verbose patch to match with upstream (don't print on history -S)
  Resolves: #672810

* Wed Jan 26 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-12
- Fix error message on exit
  Resolves: #672810

* Mon Jan 24 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-11
- Don't set $REMOTEHOST on the local machine
  Resolves: #669176
- Don't print history in verbose mode
  Resolves: #583075, #658171
- Don't allow illegal variable names to be set
  Resolves: #436901
- Revert "Fix incorrect $status value of pipelined commands"

* Tue Dec 21 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-10
- Make wait builtin command interruptible
  Resolves: #440465
- Fix incorrect $status value of pipelined commands
  Resolves: #638955 (Patch by Tomas Smetana <tsmetana@redhat.com>)

* Wed Oct  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-9
- Remove fork when tcsh processes backquotes

* Wed Apr 14 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-8
- Fix testsuite

* Mon Mar  1 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-7
- Ship README file

* Tue Dec 15 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-6
- Fix tcsh obeys printexitvalue for back-ticks

* Wed Nov  4 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-5
- Fix few globbing problems

* Mon Oct 19 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-4
- Fix tcsh globbing causing bad automount
- Fix truncated history file after network crash

* Wed Aug 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-3
- Add new colorls variable
  Resolves: #518808

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-1
- Update to tcsh-6.17.00

* Thu Apr 30 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.16-1
- Update to tcsh-6.16.00
- Merge Review (fix License, add BUGS and WishList to documentation, convert Fixes and
  WishList to UTF-8, remove root checking from buildroot cleaning, preserve timestamps,
  use smp_flags, remove unused patches, improve postun script and minor fix to %%files)
  Resolves: #226483

* Mon Mar  2 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-8
- Fix tcsh needs to know about new colorls variables
  Resolves: #487783

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-6
- Fix UTF-8 Japanese character is garbled in tcsh script in
  a certain situation
  Related: #453785
- Fix calculation order of operators description in tcsh manpage
  Related: #442536
- Fix strings which begin with '0' are not recognized as octal numbers
  Related: #438109
- Fix memoryuse description in tcsh manpage
  Related: #437095
- Fix tcsh scripts with multiple case statement with end keywords
  break with error
  Related: #436956
- Fix description of builtin command 'set' in tcsh manpage
  Related: #430459

* Fri Aug 29 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-5
- Rediffed all patches to work with patch --fuzz=0
- Let tcsh know 'ca' colorls variable
  Resolves: #458716

* Fri Feb 29 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-4
- Fix '\' can not be used to quote all delimiters
  Related: #435421
- Fix $name[selector] should fail when any number of 'selector' is out of range
  Related: #435398

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-3
- Fix Buildroot

* Fri Jan 18 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-2
- Rebuild

* Mon Aug 27 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-1
- Update to tcsh-6.15.00
- Fix license
- Add gettext-devel to BuildRequires (AM_ICONV)

* Wed Apr 25 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.14-16
- Fix floating exception in print_by_column() with unprintable characters
  (#233525)

* Mon Feb 26 2007 Miloslav Trmac <mitr@redhat.com> - 6.14-15
- Fix License:
  Related: #226483.

* Mon Feb 12 2007 Miloslav Trmac <mitr@redhat.com> - 6.14-14
- Link to libtinfo instead of libncurses

* Thu Nov 30 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-13
- Link to ncurses instead of libtermcap
- Fix some rpmlint warnings

* Tue Sep 26 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-12
- Fix error handling in tcsh-6.14.00-wide-seeks.patch

* Sat Sep  9 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-11
- Fix an unlikely crash on startup (#188279)

* Wed Aug 16 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-10
- Fix an uninitialized variable causing stack corruption (#197968)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.14-9.1
- rebuild

* Mon Jul 10 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-9
- Fix seeking over multibyte characters (#195972)
- Don't ship obsolete eight-bit.txt

* Thu Mar 23 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-8
- Backport a patch to ignore LS_COLOR codes introduced in newer coreutils
  (#186037)

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-7
- Fix a crash when reading scripts with multibyte characters (#183267)
- Block SIGINT while waiting for children (#177366)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.14-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.14-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Aug  5 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-5
- Fix EOF handling in $< (#165095, patch by s_h_o_@hotmail.co.jp)

* Thu Jul  7 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-3
- Fix -n (#162187)

* Mon Jun 20 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-2
- Backport a column width calculation bugfix (#160760)

* Fri Mar 25 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-1
- Update to tcsh-6.14.00

* Sat Mar  5 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-13
- Rebuild with gcc 4

* Fri Feb 25 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-12
- Don't ship the HTML documentation (generated from the man page, contains
  also a copy of the man page)

* Sun Jan 30 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-11
- Fix the previous patch, handle a missed case (#146330)

* Sat Jan 15 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-10
- Avoid reusing iconv_catgets' static buffer (#145177, #145195)

* Tue Sep 21 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-9
- Fix invalid argument to xprintf () (#133129)

* Wed Sep 15 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-8
- Fix $HOSTTYPE and $MACHTYPE for ppc64 and s390x, this time for sure

* Wed Sep 15 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-7
- Define $HOSTTYPE and $MACHTYPE for ppc64 and s390 (#115531),
  I hope that finally covers all architectures.

* Wed Sep 15 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-6
- Define $HOSTTYPE and $MACHTYPE also on IA-64 and s390x (#115531)
- Don't close sockets to avoid file descriptor conflits with nss_ldap (#112453)

* Tue Sep 14 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-5
- Fix HTML documentation generation, second attempt (#60664)
- Set dspmbyte using nl_langinfo(CODESET) if possible, should cover all
  cases where lang.csh was correctly setting dspmbyte (#89549)

* Wed Sep  8 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-4
- Remove unneeded patches

* Thu Aug 26 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-3
- Check for SIGWINCH more often (from tcsh-6.13.01, #130941)

* Wed Aug 18 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-2
- Make comparisons for ranges in bracket expressions symmetric (#59493)
- Run perl2html with LC_ALL=C to workaround what seems to be a perl bug
  (#60664)
- Define $HOSTTYPE and $MACHTYPE on x86_64 (#115531)
- Fix setting of O_LARGEFILE (#122558)

* Tue Aug 17 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-1
- Update to tcsh-6.13.00
- Fix charset headers in some of the translations
- Convert translated messages to LC_CTYPE locale
- Fix automatic dspmbyte setting

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 6.12-7
- remove declaration of setpgrp() which conflicts with libc's (#115185)

* Fri Nov 21 2003 Nalin Dahyabhai <nalin@redhat.com> 6.12-6
- add missing buildprereqs on groff, libtermcap-devel (#110599)

* Tue Jul  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- update URL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 6.12-3
- Merge changes from 8.0-hammer

* Tue Nov 19 2002 Nalin Dahyabhai <nalin@redhat.com> 6.12-3
- rebuild

* Thu Aug 08 2002 Phil Knirsch <pknirsch@redhat.com> 6.12-2
- Added csh.1 symlink to manpages.

* Tue Jun  4 2002 Nalin Dahyabhai <nalin@redhat.com> 6.11-1
- update to 6.11

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 31 2002 Bill Nottingham <notting@redhat.com>
- rebuild in new env

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Mar 28 2001 Akira TAGOH <tagoh@redhat.com> 6.10-5
- Fixed check locale.

* Tue Feb  6 2001 Adrian Havill <havill@redhat.com>
- use <time.h> instead of <sys/time.h> for pickier lib (#25935)
- allow arguments for login shells (#19926)

* Thu Nov 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 6.10.00 to fix here-script vulnerability

* Wed Sep 18 2000 Adrian Havill <havill@redhat.com>
- fix catalog locale dirname for Japanese

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- add locale support (#10345).

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- append entries to spanking new /etc/shells.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- update to 6.09.
- fix strcoll oddness (#6000, #6244, #6398).

* Sat Sep 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix $shell by using --bindir

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Cristian Gafton <gafton@redhat.com>
- patch for using PATH_MAX instead of some silly internal #defines for
  variables that handle filenames.

* Fri Nov  6 1998 Jeff Johnson <jbj@redhat.com>
- update to 6.08.00.

* Fri Oct 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 6.07.09 from the freebsd
- security fix

* Wed Aug  5 1998 Jeff Johnson <jbj@redhat.com>
- use -ltermcap so that /bin/tcsh can be used in single user mode w/o /usr.
- update url's

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 6.07; added BuildRoot
- cleaned up the spec file; fixed source url

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- added termios hacks for new glibc
- added /bin/csh to file list

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
 - Provides csh, adds and removes /bin/csh from /etc/shells if csh package
isn't installed.
