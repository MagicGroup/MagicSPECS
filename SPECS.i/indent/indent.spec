# -*- coding: utf-8 -*-
Summary: A GNU program for formatting C code
Summary(zh_CN.UTF-8): 格式化 C 代码的 GNU 程序
Name: indent
Version: 2.2.11
Release: 5%{?dist}
License: GPLv3+
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
URL: http://indent.isidore-it.eu/beautify.html
Source: http://indent.isidore-it.eu/%{name}-%{version}.tar.gz
Patch5: indent-2.2.9-lcall.patch
Patch7: indent-2.2.9-man.patch
BuildRequires: texinfo texi2html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /usr/sbin/install-info
Requires(preun): /usr/sbin/install-info

%description
Indent is a GNU program for beautifying C code, so that it is easier to
read.  Indent can also convert from one C writing style to a different
one.  Indent understands correct C syntax and tries to handle incorrect
C syntax.

Install the indent package if you are developing applications in C and
you want a program to format your code.

%description -l zh_CN.UTF-8
格式化 C 代码的 GNU 程序。可以转换编写代码的不同风格，还可以修正 C 代码语法。


%prep
%setup -q
%patch5 -p1
%patch7 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir $RPM_BUILD_ROOT/%{_bindir}/texinfo2man \
	$RPM_BUILD_ROOT/usr/doc/indent/indent.html
magic_rpm_clean.sh
%find_lang %name

%check
echo ====================TESTING=========================
make -C regression
echo ====================TESTING END=====================

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/install-info %{_infodir}/indent.info.gz %{_infodir}/dir --entry="* indent: (indent).				Program to format source code." >/dev/null 2>&1 || :

%preun
if [ "$1" = 0 ]; then
	/usr/sbin/install-info --delete %{_infodir}/indent.info.gz %{_infodir}/dir --entry="* indent: (indent).				Program to format source code." >/dev/null 2>&1 || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README ChangeLog*
%{_bindir}/indent
%{_mandir}/man1/indent.*
%{_infodir}/indent.info*


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.2.11-5
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 2.2.11-4
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010 Petr Pisar <ppisar@redhat.com> - 2.2.11-2
- Clean spec file from commented code

* Tue Jul 20 2010 Petr Pisar <ppisar@redhat.com> - 2.2.11-1
- 2.2.11 bump (#457064)
- Remove useless patches: indent-2.2.9-cdw.patch, indent-2.2.9-explicits.patch
- Reenable parallel build
- Distribute upstream changelogs

* Tue Aug 11 2009 Roman Rakus <rrakus@redhat.com> - 2.2.10-5
- Don't print errors in post and preun sections (#515935)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.10-2
- Cleared man patch to comply with fuzz=0
  Resolves: #465015

* Wed Mar 12 2008 Petr Machata <pmachata@redhat.com> - 2.2.10-1
- Rebase to 2.2.10
  - Dropped three patches
  - Fix Source and URL
  - Clean up spec

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.9-19
- Autorebuild for GCC 4.3

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 2.2.9-18
- Fix licensing tag.

* Fri Feb  2 2007 Petr Machata <pmachata@redhat.com> - 2.2.9-17
- Tidy up the specfile per rpmlint comments
- Use utf-8 and fix national characters in contributor's names

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 2.2.9-15
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223703

* Mon Jul 17 2006 Karsten Hopp <karsten@redhat.de> 2.2.9-14
- add buildrequires makeinfo

* Sun Jul 16 2006 Petr Machata <pmachata@redhat.com> - 2.2.9-13
- Add some missing options to manpage/infopage (#199037)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.9-12.3.1
- rebuild

* Tue Jun  6 2006 Petr Machata <pmachata@redhat.com> - 2.2.9-12.3
- BuildRequires gettext

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.9-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.9-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Feb 02 2006 Petr Machata <pmachata@redhat.com> 2.2.9-12
- Adding Wei-Lun Chao's zh_TW UTF-8 messages (#134044)

* Wed Feb 01 2006 Petr Machata <pmachata@redhat.com> 2.2.9-11
- Setting LC_ALL instead of LC_MESSAGES in order to fix output of
  KOI8-R characters.  (#134044)

* Wed Jan 27 2006 Petr Machata <pmachata@redhat.com> 2.2.9-10
- Changed the placement of closing `while' of `do {} while' command
  under a -cdw option.  It's now cuddled up to the brace. (#67781)
- Changed the indentation of cuddled `else': the brace is lined up
  under opening brace.  Let's see if people like it.  It looks less
  strange than before, but still it looks strange.

* Wed Jan 18 2006 Petr Machata <pmachata@redhat.com> 2.2.9-9
- Silenting some warnings, voidifying some functions that were
  implicitly int but didn't actually return anything. (#114376)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Apr 10 2005 Jakub Jelinek <jakub@redhat.com> 2.2.9-8
- add %%check

* Sun Apr 10 2005 Jakub Jelinek <jakub@redhat.com> 2.2.9-7
- rebuilt with GCC4
- fixed source URL

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 03 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add a bugfix (copied from debian)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.9

* Wed Nov 27 2002 Elliot Lee <sopwith@redhat.com> 2.2.8-4
- Don't use wildcard on bindir

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.8

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.7-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.7
- use find_lang for translations
- do not gzip man-page

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Nov 19 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2.6

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%configure, %%makeinstall, %%{_infodir}, %%{_mandir} 
  and %%{_tmppath}
- don't use %%{_prefix}

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added URL
- remove manual stripping


* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed

* Thu Jan 20 2000 Bill Nottingham <notting@redhat.com>
- 2.2.5

* Mon Jul 26 1999 Bill Nottingham <notting@redhat.com>
- 2.2.0

* Fri Jul 16 1999 Bill Nottingham <notting@redhat.com>
- update to 2.1.1

* Sun May 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.0.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 11)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- use install-info

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
