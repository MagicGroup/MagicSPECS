Summary: POSIX File System Archiver
Summary(zh_CN.UTF-8): POSIX 文件系统归档
Name: pax
Version: 3.4
Release: 18%{?dist}
License: BSD
Group: Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
Source: ftp://ftp.suse.com/pub/people/kukuk/pax/%{name}-%{version}.tar.bz2
URL:    ftp://ftp.suse.com/pub/people/kukuk/pax/
#use Linux PATH_MAX (4092) for maximum PATHLENGTH instead of pax default 3072
Patch0: pax-3.0-PATHMAX.patch
#fix bug with archiving files of filename length exactly 100 chars
Patch1: pax-3.4-abs100.patch
#do not truncate names when extracting
Patch2: pax-3.4-rdtruncate.patch
#do not fail with gcc-4.6+
Patch3: pax-gcc46.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
'pax' is the POSIX standard archive tool.  It supports the two most
common forms of standard Unix archive (backup) files - CPIO and TAR.

%description -l zh_CN.UTF-8
POSIX 标准归档工具，支持两种 Unix 常用归档文件 - CPIO 和 TAR。

%prep
%setup -q
%patch0 -p1 -b .PATHMAX
%patch1 -p1 -b .abs100
%patch2 -p1 -b .rdtruncate
%patch3 -p1 -b .gcc46

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS ChangeLog COPYING NEWS README THANKS
%{_bindir}/pax
%doc %{_mandir}/man1/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 3.4-18
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.4-17
- 为 Magic 3.0 重建

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 3.4-16
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.4-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Ondrej Vasik <ovasik@redhat.com> - 3.4-12
- fix FTBFS with gcc4.6+ - (#715754)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ondrej Vasik <ovasik@redhat.com> - 3.4-8
- Merge review #226235: fix use of %%makeinstall as well

* Mon Jan 19 2009 Ondrej Vasik <ovasik@redhat.com> - 3.4-7
- Merge review #226235: do ship doc files,
  do comment patches, use better buildroot and
  defaults for attributes, allow parallel builds

* Fri Aug 29 2008 Ondrej Vasik <ovasik@redhat.com> - 3.4-6
- removed duplicate Source0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.4-5
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.4-4
- Rebuild for selinux ppc32 issue.

* Mon Jul 16 2007 Radek Brich <rbrich@redhat.com> - 3.4-3
- do not truncate file names when extracting (#205324)

* Wed Jun 20 2007 Radek Brich <rbrich@redhat.com> - 3.4-2
- applied patch for #239000 (pax fails creation of ustar
  if an absolute name is exactly 100 characters long)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.4-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.4-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 15 2005 Peter Vrabec <pvrabec@redhat.com> 3.4-1
- upgrade 3.4

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com> 3.0-11
- rebuilt

* Thu Oct 21 2004 Peter Vrabec <pvrabec@redhat.com>
- fix PAXPATHLEN (#132857)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 3.0-5
- rebuild on all arches

* Wed Jul 03 2002 Karsten Hopp <karsten@redhat.de>
- fix documentation (#63671)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar  5 2002 Matt Wilson <msw@redhat.com>
- pull PAX source tarball from the SuSE package (which is based off
  this one yet claims copyright on the spec file)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Feb 23 2001 Jakub Jelinek <jakub@redhat.com>
- make it build under glibc 2.2.2

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Preston Brown <pbrown@redhat.com>
- debian version, which is a port from OpenBSD's latest.

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Tue May 30 2000 Preston Brown <pbrown@redhat.com>
- adopted for Winston.

