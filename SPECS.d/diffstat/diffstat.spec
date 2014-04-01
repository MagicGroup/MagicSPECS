Summary: A utility which provides statistics based on the output of diff
Summary(zh_CN.UTF-8): 提供基于 diff 输出统计的工具
Name: diffstat
Version: 1.58
Release: 4%{?dist}
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License: MIT
URL: http://invisible-island.net/diffstat
Source0: ftp://invisible-island.net/diffstat/%{name}-%{version}.tgz
# Taken from diffstat.c.
Source1: COPYING
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: xz

%description
The diff command compares files line by line.  Diffstat reads the
output of the diff command and displays a histogram of the insertions,
deletions and modifications in each file.  Diffstat is commonly used
to provide a summary of the changes in large, complex patch files.

Install diffstat if you need a program which provides a summary of the
diff command's output.

%description -l zh_CN.UTF-8
提供基于 diff 输出统计的工具。

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
cp %{SOURCE1} .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING CHANGES README
%{_bindir}/diffstat
%{_mandir}/*/*

%changelog
* Thu Mar 20 2014 Liu Di <liudidi@gmail.com> - 1.58-4
- 更新到 1.58

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.54-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Tim Waugh <twaugh@redhat.com> 1.54-1
- 1.54.

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> 1.51-2
- Added comment for COPYING file.

* Mon Nov  9 2009 Tim Waugh <twaugh@redhat.com> 1.51-1
- 1.51.

* Sat Oct 31 2009 Tim Waugh <twaugh@redhat.com> 1.50-1
- 1.50 (bug #527702).
- Ship CHANGES and README (bug #527703).
- Build requires xz (bug #527708).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.43-8
- fix license tag

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 1.43-7
- Rebuild for GCC 4.3.

* Thu Aug 23 2007 Tim Waugh <twaugh@redhat.com> 1.43-6
- Rebuilt.

* Fri Mar 23 2007 Tim Waugh <twaugh@redhat.com> 1.43-5
- Fixed description (bug #225695).

* Mon Mar 12 2007 Tim Waugh <twaugh@redhat.com> 1.43-4
- Removed unnecessary comment (bug #225695).
- Fixed license tag (bug #225695).

* Tue Mar  6 2007 Tim Waugh <twaugh@redhat.com> 1.43-3
- Fixed source0 (bug #225695).
- Added COPYING file, taken from diffstat.c.

* Tue Mar  6 2007 Tim Waugh <twaugh@redhat.com> 1.43-2
- Fixed buildroot (bug #225695).
- Build should not require gzip or bzip2 as these are exceptions (bug #225695).
- Added SMP make flags (bug #225695).
- Avoid makeinstall macro (bug #225695).
- Better defattr (bug #225695).
- Fixed summary (bug #225695).
- Avoid macros in changelog (bug #225695).

* Thu Jan 11 2007 Tim Waugh <twaugh@redhat.com> 1.43-1
- 1.43.  Fixes bug #187350.  No longer need compress patch.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.41-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.41-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.41-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Tim Waugh <twaugh@redhat.com> 1.41-1
- 1.41.
- Corrected URL.

* Wed Aug 10 2005 Tim Waugh <twaugh@redhat.com> 1.38-4
- Handle .Z files (bug #165507).

* Tue Jul 26 2005 Tim Waugh <twaugh@redhat.com> 1.38-3
- Fixed man page location (bug #164296).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1.38-2
- Rebuild for new GCC.

* Wed Feb  2 2005 Tim Waugh <twaugh@redhat.com> 1.38-1
- 1.38 (bug #146857).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Oct 17 2002 Tim Waugh <twaugh@redhat.com> 1.31-1
- 1.31.  Fixes bug #74971.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May  3 2001 Tim Waugh <twaugh@redhat.com>
- Fix URL.
- 1.28.  Makefile patch no longer needed.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- use rpm macros

* Wed May 31 2000 Ngo Than <than@redhat.de>
- rebuild for 7.0
- put man page in /usr/share/man/*
- use %%configure
- fix makefile.in
- cleanup specfile

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- gzip man page.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.27, add URL tag.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
