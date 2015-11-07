Summary: Revision Control System (RCS) file version management tools
Summary(zh_CN.UTF-8): 版本控制系统 (RCS) 文件版本管理工具
Name: rcs
Version:	5.9.4
Release:	2%{?dist}
License: GPLv3+
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
URL: http://www.gnu.org/software/rcs/
Source: http://mirrors.ustc.edu.cn/gnu/rcs/%{name}-%{version}.tar.xz
Patch0: rcs-5.8-build-tweaks.patch
Patch2: rcs-5.8-newsvnsyntax.patch
Provides: bundled(gnulib)
BuildRequires: autoconf
BuildRequires: groff
BuildRequires: ghostscript
BuildRequires: sendmail
BuildRequires: ed
Requires: diffutils
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description
The Revision Control System (RCS) is a system for managing multiple
versions of files.  RCS automates the storage, retrieval, logging,
identification and merging of file revisions.  RCS is useful for text
files that are revised frequently (for example, programs,
documentation, graphics, papers and form letters).

The rcs package should be installed if you need a system for managing
different versions of files.

%description -l zh_CN.UTF-8
版本控制系统 (RCS) 文件版本管理工具。

%prep
%setup -q
%patch0 -p1 -b .build-tweaks
%patch2 -p1 -b .newsvnsyntax
autoconf

%build
%configure --with-diffutils
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

install -m 755 src/rcsfreeze $RPM_BUILD_ROOT%{_bindir}

rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
magic_rpm_clean.sh

%check
make check

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :


%postun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :
fi

%files
%doc ChangeLog COPYING THANKS NEWS README
%{_bindir}/*
%{_mandir}/man[15]/*
%{_infodir}/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 5.9.4-2
- 为 Magic 3.0 重建

* Sat Sep 12 2015 Liu Di <liudidi@gmail.com> - 5.9.4-1
- 更新到 5.9.4

* Fri Nov 23 2012 Honza Horak <hhorak@redhat.com> - 5.8.1-4
- Use make DESTDIR=... install instead of %%make_install

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Honza Horak <hhorak@redhat.com> - 5.8.1-2
- Provides: bundled(gnulib) added, as per #821786
- minor spec file clean up
- install-info run in postin/postun

* Wed Jun 06 2012 Honza Horak <hhorak@redhat.com> - 5.8.1-1
- Update to upstream 5.8.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Honza Horak <hhorak@redhat.com> - 5.8-1
- Update to upstream 5.8
- Dropped patches -security, -DESTDIR and -option that are not needed 
  anymore
- Run tests in %%check

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2010 Ville Skyttä <ville.skytta at iki.fi> - 5.7-36
- Add dependency on diffutils.
- Apply build tweaks patch from Debian (incl installing rcsfreeze).
- BuildRequire autoconf instead of automake.
- Actually configure instead of shipping a pregenerated conf.h (#226356).
- Ship docs as PDF rather than troff source.
- Run test suite during build.
- Include COPYING.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.7-33
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.7-32
- Autorebuild for GCC 4.3

* Tue Jul 17 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 5.7-31
- Addded support for new svn syntax.
- Resolves: #247998

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.7-30.1
- rebuild

* Mon Jun 12 2006 Jesse Keating <jkeating@redhat.com> - 5.7-30
- Add missing BR automake

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.7-29.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.7-29.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Phil Knirsch <pknirsch@redhat.com> 5.7-29
- Fixed bug with obsolete and changed -u option for diff (#165071)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 5.7-28
- bump release and rebuild with gcc 4

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com> 5.7-27
- add spec change from #144485

* Tue Sep 21 2004 Phil Knirsch <pknirsch@redhat.com> 5.7-26
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 5.7-25
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.7-24
- rebuilt

* Wed Feb 04 2004 Phil Knirsch <pknirsch@redhat.com> 5.7-23
- Switched copyright to license. :-)

* Fri Oct 31 2003 Phil Knirsch <pknirsch@redhat.com> 5.7-22
- Included sameuserlocks patch from James Olin Oden (#107947).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 5.7-19
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- tmpfile security patch from Olaf Kirch <okir@lst.de>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file; added BuildRoot

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
-built against glibc
