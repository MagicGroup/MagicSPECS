Summary: Utility for the creation of squashfs filesystems
Name: squashfs-tools
Version: 4.2
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Base
URL: http://squashfs.sourceforge.net/
Source0: http://downloads.sourceforge.net/squashfs/squashfs%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: lzo-devel
BuildRequires: libattr-devel

%description
Squashfs is a highly compressed read-only filesystem for Linux.  This package
contains the utilities for manipulating squashfs filesystems.

%prep
%setup -q -n squashfs4.2

%build
pushd squashfs-tools
CFLAGS="%{optflags}" XZ_SUPPORT=1 LZO_SUPPORT=1 LZMA_XZ_SUPPORT=1 make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/sbin %{buildroot}/usr/sbin
install -m 755 squashfs-tools/mksquashfs %{buildroot}/sbin/mksquashfs
install -m 755 squashfs-tools/unsquashfs %{buildroot}%{_sbindir}/unsquashfs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README ACKNOWLEDGEMENTS DONATIONS PERFORMANCE.README README-4.2 CHANGES pseudo-file.example COPYING

/sbin/mksquashfs
%{_sbindir}/unsquashfs

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.2-3
- 为 Magic 3.0 重建

* Thu Feb 09 2012 Liu Di <liudidi@gmail.com> - 4.2-2
- 为 Magic 3.0 重建

* Tue Mar 01 2011 Bruno Wolff III <bruno@wolff.to> - 4.2-1
- 4.2 is released.
- Bugfix for bad data causing crash.
- Include doc files added for release.
- Big endian patch is now upstream.
- Buildroot tag isn't needed any more.
- We can now specify CFLAGS on the make call.
- Compressor options are now passed with the make call.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-0.4.20101231
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Dan Horák <dan[at]danny.cz> - 4.2-0.3.20101231
- Add fixes for big-endian machines

* Sat Jan 01 2011 Bruno Wolff III <bruno@wolff.to> - 4.2-0.2.20101231
- Pull latest upstream snapshot
- Includes check for matching compression type when adding to an existing image
- Sample cvs command now includes timezone and specifies when on the date to use for the snapshot

* Fri Dec 24 2010 Bruno Wolff III <bruno@wolff.to> - 4.2-0.1.20101223
- Switch to 4.2 development snapshot to get new XZ support
- LZMA and XZ (LZMA2) support are now different

* Wed Oct 27 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-3
- Rebuild for xz soname bump

* Wed Sep 29 2010 jkeating - 4.1-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-1
- Update to 4.1 final.
- Byte swap patch is now upstream.
- LZO compression type is now supported.

* Mon Sep 6 2010 Dan Horák <dan[at]danny.cz> - 4.1-0.5.20100827
- Add fixes for big-endian machines

* Sat Aug 28 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.4.20100827
- Rebase to latest upstream.
- The main reason is to pick up a fix for large xattr similar to the large inode fix. This doesn't need to get backported as 4.0 doesn't have xattr support.
- An option was added to build without xattr support.
- Various source cleanups have been done as well.

* Tue Aug 03 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.3.20100803
- Rebase to latest upstream
- Prevent warning message for xattr for virtual directory
- Fix issue with large inodes - BZ 619020

* Wed Jul 27 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.2.20100727
- Rebase to latest upstream devel state. Mostly xattr fixes and cleanup.

* Wed Jun 08 2010 Bruno Wolff III <bruno@wolff.to> - 4.1-0.1.20100607
- Rebase to 4.1 prerelease with xz wrapper
- Provides lzma compression as an option.
- squashfs-fix-unsquashing-v3.patch is part of the 4.1 prerelease

* Wed May 5 2010 Kyle McMartin <kyle@redhat.com> 4.0-4
- squashfs-fix-unsquashing-v3.patch: pull in fix from cvs. Thanks pkl!
  (rhbz#523504)

* Thu Feb 18 2010 Kyle McMartin <kyle@redhat.com> 4.0-3
- Update to release tarball as opposed to cvs snapshot.
- Add dist tag.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 05 2009 Kyle McMartin <kyle@redhat.com> - 4.0-1
- Update to release 4.0

* Tue Mar 16 2009 Kyle McMartin <kyle@redhat.com> - 4.0-0.20090316
- update to cvs snap from 2009-03-16.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-0.20090126
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kyle McMartin <kyle@redhat.com> - 4.0-0.20090125
- update to cvs snap that should unbreak big endian machines creating
  little endian fs.

* Mon Jan 12 2009  <katzj@redhat.com> - 4.0-0.20090112
- update to cvs snap that generates v4.0 images

* Tue Sep 30 2008 Jeremy Katz <katzj@redhat.com> - 3.4-1
- update to 3.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.3-2
- Autorebuild for GCC 4.3

* Fri Dec 14 2007 Jeremy Katz <katzj@redhat.com> - 3.3-1
- Update to 3.3

* Wed Sep  5 2007 Jeremy Katz <katzj@redhat.com> - 3.2-2
- fixes from package review (#226430)

* Tue Mar 20 2007 Jeremy Katz <katzj@redhat.com> - 3.2-1
- update to 3.2r2

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 3.0-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Jeremy Katz <katzj@redhat.com> - 3.0-3
- updated fragment size patch (#204638)

* Wed Aug 16 2006 Jeremy Katz <katzj@redhat.com> - 3.0-2
- add upstream patch for fragment size problem (#202663)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0-1.1
- rebuild

* Fri Jun 23 2006 Jeremy Katz <katzj@redhat.com> - 3.0-1
- update to 3.0
- include unsquashfs

* Tue May 16 2006 Jeremy Katz <katzj@redhat.com> 
- add BR on zlib-devel (Andreas Thienemann, #191880)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2r2-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2r2-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Jeremy Katz <katzj@redhat.com> - 2.2r2-1
- Initial build

