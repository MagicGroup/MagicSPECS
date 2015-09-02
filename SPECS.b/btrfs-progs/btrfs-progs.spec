Name:		btrfs-progs
Version:	4.1.2
release:	1%{?dist}
Summary:	Userspace programs for btrfs

Group:		System Environment/Base
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/%{name}/%{name}-v%{version}.tar.xz

# Patches no longer applied, but kept for posterity
# Still must reverse-engineer fixes in there and get upstream
Patch0:		btrfs-progs-valgrind.patch
Patch1:		btrfs-init-dev-list.patch
# Applied
Patch2:		btrfs-mkfs-missing-exit.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf, automake
BuildRequires:	e2fsprogs-devel, libuuid-devel, zlib-devel
BuildRequires:	libacl-devel, libblkid-devel, lzo-devel
BuildRequires:	asciidoc, xmlto

%define _root_sbindir /sbin

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package devel
Summary:	btrfs filesystem-specific libraries and headers
Group:		Development/Libraries
Requires:	btrfs-progs = %{version}-%{release}

%description devel
btrfs-progs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

You should install btrfs-progs-devel if you want to develop
btrfs filesystem-specific programs.

%prep
%setup -q -n %{name}-v%{version}

%patch2 -p1

%build
./autogen.sh
%configure CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make mandir=%{_mandir} bindir=%{_sbindir} libdir=%{_libdir} incdir=%{_includedir}/btrfs install DESTDIR=$RPM_BUILD_ROOT
# Nuke the static lib
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libbtrfs.so.0*
%{_sbindir}/btrfsck
%{_sbindir}/fsck.btrfs
%{_sbindir}/mkfs.btrfs
%{_sbindir}/btrfs-debug-tree
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfs-select-super
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-zero-log
%{_sbindir}/btrfs-find-root
%{_sbindir}/btrfs-show-super
%{_mandir}/man5/*.gz
%{_mandir}/man8/*.gz

%files devel
%{_includedir}/*
%{_libdir}/libbtrfs.so

%changelog
* Thu Aug 06 2015 Eric Sandeen <sandeen@redhat.com> 4.1.2-1
- New upstream release
- Fix to reject unknown mkfs options (#1246468)

* Mon Jun 22 2015 Eric Sandeen <sandeen@redhat.com> 4.1-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Eric Sandeen <sandeen@redhat.com> 4.0.1-1
- New upstream release

* Wed Apr 29 2015 Eric Sandeen <sandeen@redhat.com> 4.0-1
- New upstream release

* Thu Mar 26 2015 Eric Sandeen <sandeen@redhat.com> 3.19.1-1
- New upstream release

* Wed Mar 11 2015 Eric Sandeen <sandeen@redhat.com> 3.19-1
- New upstream release

* Tue Jan 27 2015 Eric Sandeen <sandeen@redhat.com> 3.18.2-1
- New upstream release

* Mon Jan 12 2015 Eric Sandeen <sandeen@redhat.com> 3.18.1-1
- New upstream release

* Fri Jan 02 2015 Eric Sandeen <sandeen@redhat.com> 3.18-1
- New upstream release

* Fri Dec 05 2014 Eric Sandeen <sandeen@redhat.com> 3.17.3-1
- New upstream release

* Fri Nov 21 2014 Eric Sandeen <sandeen@redhat.com> 3.17.2-1
- New upstream release

* Mon Oct 20 2014 Eric Sandeen <sandeen@redhat.com> 3.17-1
- New upstream release

* Fri Oct 03 2014 Eric Sandeen <sandeen@redhat.com> 3.16.2-1
- New upstream release
- Update upstream source location

* Wed Aug 27 2014 Eric Sandeen <sandeen@redhat.com> 3.16-1
- New upstream release

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Eric Sandeen <sandeen@redhat.com> 3.14.2-3
- Support specification of UUID at mkfs time (#1094857)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Eric Sandeen <sandeen@redhat.com> 3.14.2-1
- New upstream release

* Tue Apr 22 2014 Eric Sandeen <sandeen@redhat.com> 3.14.1-1
- New upstream release

* Wed Apr 16 2014 Eric Sandeen <sandeen@redhat.com> 3.14-1
- New upstream release

* Mon Jan 20 2014 Eric Sandeen <sandeen@redhat.com> 3.12-2
- Add proper Source0 URL, switch to .xz

* Mon Nov 25 2013 Eric Sandeen <sandeen@redhat.com> 3.12-1
- It's a new upstream release!

* Thu Nov 14 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20131114git9f0c53f-1
- New upstream snapshot

* Tue Sep 17 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130917git194aa4a-1
- New upstream snapshot
- Deprecated btrfsctl, btrfs-show, and btrfs-vol; still available in btrfs cmd

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.rc1.20130501git7854c8b-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Richard W.M. Jones <rjones@redhat.com> 0.20.rc1.20130501git7854c8b-3
- Add accepted upstream patch to fix SONAME libbtrfs.so -> libbtrfs.so.0

* Thu May 02 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130501git7854c8b-2
- Fix subpackage brokenness

* Wed May 01 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130501git7854c8b-1
- New upstream snapshot
- btrfs-progs-devel subpackage

* Fri Mar 08 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130308git704a08c-1
- New upstream snapshot
- btrfs-restore is now a command in the btrfs utility

* Wed Feb 13 2013 Richard W.M. Jones <rjones@redhat.com> 0.20.rc1.20121017git91d9eec-3
- Include upstream patch to clear caches as a partial fix for RHBZ#863978.

* Thu Nov  1 2012 Josef Bacik <josef@toxicpanda.com> 0.20.rc1.20121017git91d9eec-2
- fix a bug when mkfs'ing a file (rhbz# 871778)

* Wed Oct 17 2012 Josef Bacik <josef@toxicpanda.com> 0.20.rc1.20121017git91d9eec-1
- update to latest btrfs-progs

* Wed Oct 10 2012 Richard W.M. Jones <rjones@redhat.com> 0.19.20120817git043a639-2
- Add upstream patch to correct uninitialized fsid variable
  (possible fix for RHBZ#863978).

* Fri Aug 17 2012 Josef Bacik <josef@toxicpanda.com> 0.19.20120817git043a639-1
- update to latest btrfs-progs

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Josef Bacik <josef@toxicpanda.com> 0.19-19
- make btrfs filesystem show <uuid> actually work (rhbz# 816293)

* Wed Apr 11 2012 Josef Bacik <josef@toxicpanda.com> 0.19-18
- updated to latest btrfs-progs

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 05 2011 Josef Bacik <josef@toxicpanda.com> 0.19-16
- fix build-everything patch to actually build everything

* Fri Aug 05 2011 Josef Bacik <josef@toxicpanda.com> 0.19-15
- actually build btrfs-zero-log

* Thu Aug 04 2011 Josef Bacik <josef@toxicpanda.com> 0.19-14
- bring btrfs-progs uptodate with upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Adam Tkac <atkac redhat com> 0.19-12
- rebuild to ensure F14 has bigger NVR than F13

* Wed Mar 24 2010 Josef Bacik <josef@toxicpanda.com> 0.19-11
- bring btrfs-progs uptodate with upstream, add btrfs command and other
  features.

* Thu Mar 11 2010 Josef Bacik <josef@toxicpanda.com> 0.19-10
- fix dso linking issue and bring btrfs-progs uptodate with upstream

* Tue Feb 2 2010 Josef Bacik <josef@toxicpanda.com> 0.19-9
- fix btrfsck so it builds on newer glibcs

* Tue Feb 2 2010 Josef Bacik <josef@toxicpanda.com> 0.19-8
- fix btrfsctl to return 0 on success and 1 on failure

* Tue Aug 25 2009 Josef Bacik <josef@toxicpanda.com> 0.19-7
- add btrfs-progs-valgrind.patch to fix memory leaks and segfaults

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Josef Bacik <josef@toxicpanda.com> 0.19-5
- add e2fsprogs-devel back to BuildRequires since its needed for the converter

* Wed Jul 15 2009 Josef Bacik <josef@toxicpanda.com> 0.19-4
- change BuildRequires for e2fsprogs-devel to libuuid-devel

* Fri Jun 19 2009 Josef Bacik <josef@toxicpanda.com> 0.19-3
- added man pages to the files list and made sure they were installed properly

* Fri Jun 19 2009 Josef Bacik <josef@toxicpanda.com> 0.19-2
- add a patch for the Makefile to make it build everything again

* Fri Jun 19 2009 Josef Bacik <josef@toxicpanda.com> 0.19-1
- update to v0.19 of btrfs-progs for new format

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Josef Bacik <josef@toxicpanda.com> 0.18-3
- updated label patch

* Thu Jan 22 2009 Josef Bacik <josef@toxicpanda.com> 0.18-2
- add a patch to handle having /'s in labels

* Sat Jan 17 2009 Josef Bacik <josef@toxicpanda.com> 0.18-1
- updated to 0.18 because of the ioctl change in 2.6.29-rc2

* Fri Jan 16 2009 Marek Mahut <mmahut@fedoraproject.org> 0.17-4
- RHBZ#480219 btrfs-convert is missing

* Mon Jan 12 2009 Josef Bacik <josef@toxicpanda.com> 0.17-2
- fixed wrong sources upload

* Mon Jan 12 2009 Josef Bacik <josef@toxicpanda.com> 0.17
- Upstream release 0.17

* Sat Jan 10 2009 Kyle McMartin <kyle@redhat.com> 0.16.git1-1
- Upstream git sync from -g72359e8 (needed for kernel...)

* Sat Jan 10 2009 Marek Mahut <mmahut@fedoraproject.org> 0.16-1
- Upstream release 0.16

* Wed Jun 25 2008 Josef Bacik <josef@toxicpanda.com> 0.15-4
-use fedoras normal CFLAGS

* Mon Jun 23 2008 Josef Bacik <josef@toxicpanda.com> 0.15-3
-Actually defined _root_sbindir
-Fixed the make install line so it would install to the proper dir

* Mon Jun 23 2008 Josef Bacik <josef@toxicpanda.com> 0.15-2
-Removed a . at the end of the description
-Fixed the copyright to be GPLv2 since GPL doesn't work anymore

* Mon Jun 23 2008 Josef Bacik <josef@toxicpanda.com> 0.15-1
-Initial build
