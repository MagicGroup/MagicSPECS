Summary: The GNU line editor
Summary(zh_CN.UTF-8): GNU 行编辑器
Name: ed
Version: 1.12
Release: 4%{?dist}
License: GPLv3+
Group:  Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
Source: ftp://ftp.gnu.org/gnu/ed/%{name}-%{version}.tar.lz
URL:    http://www.gnu.org/software/ed/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: /bin/ed, /bin/red

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it.

%description -l zh_CN.UTF-8
GNU 行编辑器，一般情况下只会被一些程序使用。

%prep
%setup -q
rm -f stamp-h.in

%build
%configure --exec-prefix=%{_prefix}
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
make install DESTDIR=$RPM_BUILD_ROOT \
    bindir=%{_bindir} mandir=%{_mandir}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir*
gzip -9qnf  $RPM_BUILD_ROOT%{_infodir}/*

magic_rpm_clean.sh

%post
/usr/sbin/install-info %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor." || :

%preun
if [ $1 = 0 ] ; then
  /usr/sbin/install-info --delete %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor." || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README TODO AUTHORS COPYING
%{_bindir}/*
%{_infodir}/ed.info.gz
%{_mandir}/*/*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.12-4
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.12-3
- 更新到 1.12

* Thu Mar 27 2014 Liu Di <liudidi@gmail.com> - 1.10-2
- 更新到 1.10

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.6-2
- 为 Magic 3.0 重建

* Thu Mar 15 2012 Karsten Hopp <karsten@redhat.com> 1.6-1
- ed-1.6

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 1.5-1
- update to version 1.5 (#630693)

* Tue Apr 20 2010 Karsten Hopp <karsten@redhat.com> 1.4-2
- drop duplicate man pages (#583178)

* Tue Mar 02 2010 Karsten Hopp <karsten@redhat.com> 1.4-1
- update to latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 29 2008 Karsten Hopp <karsten@redhat.com> 1.1-1
- update to latest version, fixes CVE-2008-3916

* Tue Jun 24 2008 Karsten Hopp <karsten@redhat.com> 0.9-1
- version 0.9

* Mon Mar 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8-2
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Karsten Hopp <karsten@redhat.com> 0.8-1
- update to 0.8

* Wed Aug 22 2007 Karsten Hopp <karsten@redhat.com> 0.7-2
- update license tags

* Mon Jul 23 2007 Karsten Hopp <karsten@redhat.com> 0.7-1
- update to 0.7 to fix an endless loop (#234689)
- add disttag

* Mon Jul 02 2007 Karsten Hopp <karsten@redhat.com> 0.6-1
- update to 0.6

* Wed Mar 14 2007 Karsten Hopp <karsten@redhat.com> 0.5-1
- version 0.5, fixes #228329

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 0.4-3
- clean up spec file for merge review (#225717)

* Wed Jan 31 2007 Karsten Hopp <karsten@redhat.com> 0.4-2
- use RPM_OPT_FLAGS, this fixes debuginfo

* Tue Jan 23 2007 Karsten Hopp <karsten@redhat.com> 0.4-1
- new upstream version

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 0.3-3
- don't abort (un)install scriptlets when _excludedocs is set (Ville Skyttä)

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 0.3-2
- fix man page permissions (#222581)

* Mon Nov 13 2006 Karsten Hopp <karsten@redhat.com> 0.3-1
- update to ed-0.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2-38.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2-38.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2-38.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 0.2-38
- build with gcc-4

* Mon Jan 03 2005 Karsten Hopp <karsten@redhat.de> 0.2-37
- spec file fix from Marcin Garski (#143723)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Karsten Hopp <karsten@redhat.de> 0.2-34
- rebuild

* Tue Jun 17 2003 Karsten Hopp <karsten@redhat.de> 0.2-33
- rebuild to fix crt*.o problems

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 17 2002 Karsten Hopp <karsten@redhat.de>č
- remove regex, use glibc's regex (#79132)

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 0.2-29
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May  6 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.2-26
- Fix build with current toolchain

* Wed Apr 03 2002 Karsten Hopp <karsten@redhat.de>
- don't use gcc -s 

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- bump version 

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Oct 15 2001 Karsten Hopp <karsten@redhat.de>
- add home page (#54602)

* Sat Jul 07 2001 Karsten Hopp <karsten@redhat.de>
- Copyright -> License
- fix URL

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 04 2000 Karsten Hopp <karsten@redhat.de>
- back out fixes for compiler warnings

* Wed Nov 29 2000 Karsten Hopp <karsten@redhat.de>
- Security bugfix (mkstemp instead of mktemp) Bugzilla #21470

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- fix typo

* Sat Jun 17 2000 Than Ngo <than@redhat.de>
- add %%defattr
- clean up specfile

* Sat May 20 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- put man pages and infos in right place

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages.

* Tue Mar 23 1999 Jeff Johnson <jbj@redhat.com>
- fix %%post syntax error (#1689).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 11)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added install-info support
- added BuildRoot
- correct URL in Source line

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
