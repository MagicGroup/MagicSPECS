%define _sbindir /sbin
%define _libdir /%{_lib}

Summary: The GNU disk partition manipulation program
Summary(zh_CN.UTF-8): GNU 磁盘分区处理程序
Name:    parted
Version: 3.2
Release: 7%{?dist}
License: GPLv3+
Group:   Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL:     http://www.gnu.org/software/parted

Source0: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source2: pubkey.jim.meyering
Source3: pubkey.phillip.susi

Patch0001: 0001-tests-Try-several-UTF8-locales.patch
Patch0002: 0002-maint-post-release-administrivia.patch
Patch0003: 0003-libparted-also-link-to-UUID_LIBS.patch
Patch0004: 0004-lib-fs-resize-Prevent-crash-resizing-FAT16-file-syst.patch
Patch0005: 0005-tests-t3000-resize-fs.sh-Add-FAT16-resizing-test.patch
Patch0006: 0006-tests-t3000-resize-fs.sh-Add-requirement-on-mkfs.vfa.patch
Patch0007: 0007-tests-Change-minimum-size-to-256MiB.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: e2fsprogs-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: texinfo
BuildRequires: device-mapper-devel
BuildRequires: libuuid-devel
BuildRequires: libblkid-devel >= 2.17
BuildRequires: gnupg
BuildRequires: git
BuildRequires: autoconf automake
BuildRequires: e2fsprogs
BuildRequires: xfsprogs
BuildRequires: dosfstools
BuildRequires: perl-Digest-CRC
BuildRequires: bc

Requires(post): /sbin/ldconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(postun): /sbin/ldconfig

# bundled gnulib library exception, as per packaging guidelines
# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(gnulib)

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.

%description -l zh_CN.UTF-8
GNU 磁盘分区处理程序，可以创建，删除，调整，移动和复制硬盘分区。

%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
gpg --import %{SOURCE2} %{SOURCE3}
gpg --verify %{SOURCE1} %{SOURCE0}
git init
git config user.email "parted-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
[ -n "%{patches}" ] && git am %{patches}
iconv -f ISO-8859-1 -t UTF8 AUTHORS > tmp; touch -r AUTHORS tmp; mv tmp AUTHORS
git commit -a -m "run iconv"

%build
autoreconf
autoconf
CFLAGS="$RPM_OPT_FLAGS -Wno-unused-but-set-variable"; export CFLAGS
%configure --disable-selinux --disable-static --disable-gcc-warnings
# Don't use rpath!
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
V=1 %{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

# Move devel package components in to the correct location
%{__mkdir} -p %{buildroot}%{_exec_prefix}/%{_lib}
%{__mv} %{buildroot}%{_libdir}/libparted.so %{buildroot}%{_exec_prefix}/%{_lib}
%{__mv} %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_exec_prefix}/%{_lib}
pushd %{buildroot}%{_exec_prefix}/%{_lib}
reallibrary="$(readlink libparted.so)"
%{__rm} -f libparted.so
ln -sf ../../%{_lib}/${reallibrary} libparted.so
popd

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_infodir}/dir
%{__rm} -rf %{buildroot}%{_bindir}/label
%{__rm} -rf %{buildroot}%{_bindir}/disk
magic_rpm_clean.sh
%find_lang %{name}


%check
export LD_LIBRARY_PATH=$(pwd)/libparted/.libs
make check


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/ldconfig
if [ -f %{_infodir}/parted.info.gz ]; then
    /sbin/install-info %{_infodir}/parted.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/parted.info.gz %{_infodir}/dir >/dev/null 2>&1 || :
fi

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS NEWS README THANKS
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_mandir}/man8/parted.8.gz
%{_mandir}/man8/partprobe.8.gz
%{_libdir}/libparted.so.*
%{_libdir}/libparted-fs-resize.so*
%{_infodir}/parted.info.gz

%files devel
%defattr(-,root,root,-)
%doc TODO doc/API doc/FAT
%{_includedir}/parted
%{_exec_prefix}/%{_lib}/libparted.so
%{_exec_prefix}/%{_lib}/pkgconfig/libparted.pc


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 3.2-7
- 为 Magic 3.0 重建

* Wed Apr 15 2015 Liu Di <liudidi@gmail.com> - 3.2-6
- 为 Magic 3.0 重建

* Fri Nov 07 2014 Brian C. Lane <bcl@redhat.com> 3.2-5
- tests: Change minimum size to 256MiB for t1700-probe-fs

* Fri Oct 31 2014 Brian C. Lane <bcl@redhat.com> 3.2-4
- Update to current master commit ac74b83 to fix fat16 resize (#1159083)
- tests: t3000-resize-fs.sh: Add requirement on mkfs.vfat (mike.fleetwood)
- tests: t3000-resize-fs.sh: Add FAT16 resizing test (mike.fleetwood)
- lib-fs-resize: Prevent crash resizing FAT16 file systems (mike.fleetwood)
- libparted: also link to UUID_LIBS (heirecka)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Brian C. Lane <bcl@redhat.com> 3.2-2
- Use a better patch to find the UTF8 locale for t0251

* Wed Jul 30 2014 Brian C. Lane <bcl@redhat.com> 3.2-1
- Rebase on upstream stable release v3.2
- Drop upstream patches.
- Patch t0251 to use en_US.UTF-8 if possible. Fedora doesn't have C.UTF-8

* Wed Jul 30 2014 Tom Callaway <spot@fedoraproject.org> 3.1.90-2
- fix license handling

* Mon Jul 28 2014 Brian C. Lane <bcl@redhat.com> 3.1.90-1
- Rebase on upstream Alpha source release
- drop included patches (all but one)
- add Phillip Susi's GPG key
- make sure gcc warnings as errors remains disabled since we use git for patches

* Mon Jul 14 2014 Brian C. Lane <bcl@redhat.com> 3.1-29
- Rebase on parted master commit 081ed98
- libparted: Add support for partition resize
- parted: add resizepart command

* Wed Jun 11 2014 Brian C. Lane <bcl@redhat.com> 3.1-28
- Rebase on parted master commit 1da239e2ebd2
- libparted: Fix bug with dupe and empty name

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.1-26
- Move dev docs to devel
- Drop duplicated/outdated docs

* Tue May 27 2014 Brian C. Lane <bcl@redhat.com> 3.1-25
- Use mkfs.xfs to create files (#1101112)

* Thu May 22 2014 Brian C. Lane <bcl@redhat.com> 3.1-24
- Add some missing patches from master and the loop label fixes
- tests: test loop labels (psusi)
- libparted: don't trash filesystem when writing loop label (psusi)
- libparted: give correct partition device name on loop labels (psusi)
- partprobe: do not skip loop labels (psusi)
- libparted: don't create partition on loop label (psusi)
- libparted: fix loop labels to not vanish (psusi)
- libparted: remove all old partitions, even if new label allows less (psusi)
- libparted: remove old partitions *first* before adding new ones (psusi)
- libparted: don't detect fat and ntfs boot sectors as dos MBR (psusi)
- Fix filesystem detection on non 512 byte sectors (psusi)
- tests: fix t2310-dos-extended-2-sector-min-offset.sh (psusi)
- libparted: remove last_usable_if_grown (psusi)

* Fri May 16 2014 Brian C. Lane <bcl@redhat.com> 3.1-23
- Fix partition naming patch for big endian systems.

* Fri May 16 2014 Brian C. Lane <bcl@redhat.com> 3.1-22
- Fix a problem with GPT Partition names using. They are UCS-2LE not UTF-16

* Fri Apr 18 2014 Brian C. Lane <bcl@redhat.com> 3.1-21
- Fix t1700 probe patch -- remove loop before making new fs

* Thu Apr 17 2014 Brian C. Lane <bcl@redhat.com> 3.1-20
- Use force for xfs in t1700 and a larger file
- Make t4100 xfs filesystem larger and sparse
- Fix part dupe with empty name
- check name when duplicating
- Add ntfs vfat hfsplus to t1700 probe test

* Wed Apr 09 2014 Brian C. Lane <bcl@redhat.com> 3.1-19
- Use little endian packing in gpt tests
- Fix integer overflows with DVH disk label

* Tue Apr 08 2014 Brian C. Lane <bcl@redhat.com> 3.1-18
- Rebase on new upstream master commit cc382c3
- Drop patches incorporated into upstream
- Still adds the various DASD patches

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 3.1-17
- Drop hfs_esp patch. Idea didn't work.

* Wed Sep 11 2013 Brian C. Lane <bcl@redhat.com> 3.1-16
- tests: Restrict gpt header munge to little-endian systems
- Add perl Digest::CRC as a build requirement so more tests will run

* Wed Sep 04 2013 Brian C. Lane <bcl@redhat.com> 3.1-15
- libparted: Flush parent device on open (#962611)

* Wed Aug 28 2013 Brian C. Lane <bcl@redhat.com> 3.1-14
- Rebasing Fedora patches with upstream master since v3.1 release
- Summary of important changes from upstream:
  - add support for a new Linux-specific GPT partition type code
  - partprobe: remove partitions when there is no partition table
  - libparted: refactor device-mapper partition sync code
  - libparted: remove extraneous blkpg add partition ped exception
  - libparted: don't probe every dm device in probe_all
- New Fedora changes:
  - libparted: Add Intel Rapid Start Technology partition flag.
  - libparted: Add UEFI System Partition flag.
  - libparted: Add hfs_esp partition flag to GPT.
  - libparted: Recognize btrfs filesystem
  - tests: Add btrfs and xfs to the fs probe test

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Brian C. Lane <bcl@redhat.com> 3.1-12
- libparted: mklabel to support EDEV DASD (#953146)
- tests: rewrite t6001 to use /dev/mapper

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Brian C. Lane <bcl@redhat.com> 3.1-10
- libparted: mklabel to support EAV DASD (#707032)
- libparted: Avoid dasd as default disk type while probe (#707032)

* Thu Nov 01 2012 Brian C. Lane <bcl@redhat.com> 3.1-9
- don't canonicalize /dev/md/ paths (#872361)

* Tue Oct 16 2012 Brian C. Lane <bcl@redhat.com> 3.1-8
- change partition UUID to use partX-UUID (#858704)
- fixup losetup usage in tests
- add support for implicit FBA DASD partitions (#707027)
- add support for EAV DASD partitions (#707032)

* Tue Sep 04 2012 Brian C. Lane <bcl@redhat.com> 3.1-7
- reallocate buf after _disk_analyse_block_size (#835601)

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 3.1-6
- Use dm_udev_wait for dm operations (#844257) (bcl)
- use largest_partnum in _dm_reread_part_table (bcl)
- set uuid on dm partitions (#832145) (bcl)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Brian C. Lane <bcl@redhat.com> 3.1-4
- Fix crash on ppc64 with GPT (#829960) (rwmj)

* Tue May 15 2012 Brian C. Lane <bcl@redhat.com> 3.1-3
- Added Provides: bundled(gnulib) (#821782)

* Wed Mar 21 2012 Brian C. Lane <bcl@redhat.com> 3.1-2
- libparted: check PMBR before GPT partition table (#805272)
- tests: add a test for the new behavior

* Tue Mar 13 2012 Brian C. Lane <bcl@redhat.com> 3.1-1
- Rebase to upstream parted v3.1
- removed merged patches
- add new libparted-fs-resize library

* Fri Feb 03 2012 Brian C. Lane <bcl@redhat.com> - 3.0-7
- Update patch for copying flags so that it is generic
- Copy pmbr_boot flag in gpt_duplicate

* Thu Feb 02 2012 Brian C. Lane <bcl@redhat.com> - 3.0-6
- gpt: add commands to manipulate pMBR boot flag (#754850)
- parted: when printing, also print the new disk flags
- tests: update tests for new disk flags output
- tests: add test for GPT PMBR pmbr_boot flag
- doc: update parted documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Brian C. Lane <bcl@redht.com> - 3.0-4
- Fix ped_disk_duplicate on GPT so that it copies the partition flags (#747947)
- Add new test to check ped_disk_duplicate on msdos, gpt, bsd disk labels
- Add e2fsprogs and dosfstools so that skipped tests will be run

* Fri Oct 07 2011 Brian C. Lane <bcl@redhat.com> - 3.0-3
- Fix handling of zero-length gpt partitions (#728949)
- Fix bug in nilfs2 probe with short partitions (#728949)
- Fix bug in hfs probe code (#714758)
- Make pc98 detection depend on specific signatures (#646053)

* Wed Jun 29 2011 Richard W.M. Jones <rjones@redhat.com> - 3.0-2
- (Re-)apply patch to fix Linux "3.0" problem.

* Tue Jun 28 2011 Brian C. Lane <bcl@redhat.com> - 3.0-1
- Update to parted v3.0
- Run autoreconf so that patches to .am files will work
- Add patch to Fix snap radius and don't allow values < 1 (#665496)
- Add tests for the snap radius fix.
- Drop patches included in upstream release

* Sun Jun  5 2011 Richard W.M. Jones <rjones@redhat.com> - 2.4-2
- Apply patch which may fix Linux "3.0" problem.

* Thu May 26 2011 Brian C. Lane <bcl@redhat.com> - 2.4-1
- Updating to latest upstream v2.4
- Drop patches included in upstream

* Fri Mar 11 2011 Brian C. Lane <bcl@redhat.com> - 2.3-8
- Add support for legacy_boot flag for GPT partitions (680562)
- Remove PED_ASSERT for dos geometry calculations (585468)

* Wed Feb 09 2011 Brian C. Lane <bcl@redhat.com> - 2.3-7
- Tell GCC to stop treating unused variable warnings as errors

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Brian C. Lanr <bcl@redhat.com> - 2.3-5
- Document the align-check command
  Resolves: #642476
- Default to 1MiB partition alignment
  Resolves: #618255

* Fri Dec 17 2010 Peter Jones <pjones@redhat.com> - 2.3-4
- Handle mac labels with differing physical/logical sector sizes better

* Wed Sep 29 2010 jkeating - 2.3-3
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Brian C. Lane <bcl@redhat.com> 2.3-2
- Add patch to handle syncing partition changes when using blkext majors
- Resolves rhbz#634980
- Related rhbz#629719

* Tue Jul 20 2010 Hans de Goede <hdegoede@redhat.com> 2.3-1
- Rebase to new upstream 2.3 release
- Drop all patches (all upstreamed)
- Recognize scsi disks with a high major as such (#611691)

* Thu May  6 2010 Hans de Goede <hdegoede@redhat.com> 2.2-5
- Also recognize recovery partitions with id 27 / on gpt (#589451)

* Fri Apr 23 2010 Hans de Goede <hdegoede@redhat.com> 2.2-4
- Properly check dm_task_run return value (#585158)
- Fix mkpartfs (ext2) on partitions >2TB (#585159)

* Mon Apr 19 2010 Hans de Goede <hdegoede@redhat.com> 2.2-3
- Add a flag for detecting diagnostics / recovery partitions (#583626)

* Tue Apr  6 2010 Hans de Goede <hdegoede@redhat.com> 2.2-2
- Parted should not canonicalize symlinks under /dev/mapper (#577824)

* Tue Mar 30 2010 Hans de Goede <hdegoede@redhat.com> 2.2-1
- New upstream version 2.2 (#577478)
- Drop all our patches (all upstreamed)

* Thu Feb 18 2010 Hans de Goede <hdegoede@redhat.com> 2.1-5
- Copy needs_clobber value in ped_disk_duplicate() (#561976)

* Wed Feb 10 2010 Hans de Goede <hdegoede@redhat.com> 2.1-4
- Don't crash when reading a DASD disk with PV's on there (#563419)
- Don't overwrite the pmbr when merely printing a gpt table (#563211)

* Sun Jan 31 2010 Hans de Goede <hdegoede@redhat.com> 2.1-3
- If a drive does not have alignment information available default
  to an alignment of 1MiB (#559639)

* Sun Jan 17 2010 Hans de Goede <hdegoede@redhat.com> 2.1-2
- Fix various memory leaks in error paths (#556012)
- Add %%check section to the specfile, invoking make check

* Mon Jan 11 2010 Hans de Goede <hdegoede@redhat.com> 2.1-1
- New upstream release 2.1
- Drop all our patches (all merged upstream)

* Sun Dec 20 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-25
- Fix crash when partitioning loopback devices (#546622)
- Drop no-cylinder-align patch:
  - its functionality is superseeded by the per disk flags
  - its only user (pyparted) has been updated to use those
  - this is not upstream so we don't want other programs to start using it

* Fri Dec 18 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-24
- Allow partitioning of loopback devices (#546622)
- Add libparted function to query maximum partition length and start
  addresses for a given disk (#533417)
- Add per disk flags functions from upstream, this is the way upstream
  has implemented the disable cylinder alignment functionality
- Add --align cmdline option to specify how to align new partitions
  see the parted man page for details (#361951)
- Make the default alignment for new partitions optimal (#361951)
- When cylinder alignment is disabled, allow use of the last (incomplete)
  cylinder of the disk (#533328)
- Don't crash when printing partition tables in Russian (#543029)
- Make parted work correctly with new lvm (#525095)

* Wed Nov 11 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-23
- Fix parted not building on s390

* Mon Nov  9 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-22
- Fix error when creating a fresh dasd disk on a dasd device
  with a corrupted dasd label (#533808)

* Fri Nov  6 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-21
- Fix a compiler warning which is causing build errors (#532425)

* Tue Nov  3 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-20
- Fix error when creating a fresh dasd disk (#532425)
- Rewrite dasd disk duplication patches, as the old old ones conflicted
  with fixing creating a fresh dasd disk

* Fri Oct 30 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-19
- Fix a segfault introduced by -18 when operating on plain files

* Thu Oct 29 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-18
- Add functions to query device / partition table alignments (#528030)

* Thu Oct  8 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-17
- Only change the partition type to 82 when setting the swap flag on dos
  labels, not when resetting it

* Tue Oct  6 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-16
- Correctly handle GPT labels on big endian machines

* Tue Oct  6 2009 Hans de Goede <hdegoede@redhat.com> 1.9.0-15
- ped_partition_is_busy() should not throw exceptions (#527035)
- msdos_partition_is_flag_available() should return 1 for swap flag (#513729)

* Mon Aug 31 2009 Joel Granados <jgranado@redhat.com> 1.9.0-14
- Patchs for 'commit to os' for linux.  Thx to hansg.

* Fri Aug 28 2009 Karsten Hopp <karsten@redhat.com> 1.9.0-13
- volkey is only 4 chars, don't overflow destination buffer with 84 chars

* Fri Aug 21 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-12
- libuuid-devel is now valid for s390 builds.

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.9.0-11
- Use xz compressed upstream tarball.

* Wed Aug 12 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-10
- Make install with exclude docs work without an error message.

* Wed Jul 29 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-9
- Add parenthesis where needed (#511907)

* Mon Jul 27 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-8
- Add the swap flag to the dos type labels

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-6
- Rebuild usiing the official tar.gz at http://ftp.gnu.org/gnu/parted/parted-1.9.0.tar.gz

* Wed Jul 22 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-5.20090721git980c
- Better handle a duplicate error.

* Tue Jul 21 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-4.20090721git980c
- New snapshot.
- Add patches to make dasd duplicate disk work.

* Sat Jul 18 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.9.0-3.20090610git32dc
- Fix a typo in the errno patch

* Mon Jul 13 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-2.20090610git32dc
- Correctly number the snapshot.

* Fri Jul 10 2009 Joel Granados <jgranado@redhat.com> - 1.9.0-1
- New version.

* Thu Mar 26 2009 Joel Granados <jgranado@redhat.com> - 1.8.8-15
- Begin to identify virtio devices.
- Actually change the partition type in msdos lables (dcantrell).

* Mon Mar 23 2009 Joel Granados <jgranado@redhat.com> - 1.8.8-14
- Correct the behavior of upated_mode functions when the ASSERT fails (thx to hansg).

* Thu Feb 26 2009 Joel Granados <jgranado@redhat.com> - 1.8.8-13
- Fix parted build for gcc-4.4

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Joel Granados <jgranado@redhat.com> - 1.8.8-12
- Avoid the calling of stat for strings that don't begin with the "/" char (#353191).

* Sat Dec 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.8.8-11
- fix typo in last patch

* Sat Dec 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.8.8-10
- enable RAID partition types on sun disklabels for sparc

* Thu Nov 06 2008 Joel Granados <jgranado@redhat.com> - 1.8.8-9
- Fix the build for the s390(x) archs (#470211).

* Thu Jun 05 2008 Peter Jones <pjones@redhat.com> - 1.8.8-8
- Fix some of the atvrecv code (and the msftres code) so that the flags
  actually stick.

* Thu Jun 05 2008 Peter Jones <pjones@redhat.com> - 1.8.8-7
- Added "atvrecv" flag patch from atv-bootloader project.

* Thu May 29 2008 Joel Granados <jgranado@redhat.com> - 1.8.8-6
- Do a better job at recognizing the dos partition. (#246423)

* Thu Apr 10 2008 David Cantrell <dcantrell@redhat.com> - 1.8.8-5
- Allow RAID or LVM partition types on BSD disklabels.
  (jay.estabrook AT hp.com, #427114)

* Thu Apr 10 2008 Peter Jones <pjones@redhat.com> - 1.8.8-4
- Don't interactively ask to fix an AlternateGPT's location when not
  at the end of the disk; this is so that disk images written to a
  usb-key can work reasonably.

* Mon Feb 04 2008 David Cantrell <dcantrell@redhat.com> - 1.8.8-3
- Fixes so parted compiles with gcc-4.3 (#431397)

* Sun Jan 13 2008 David Cantrell <dcantrell@redhat.com> - 1.8.8-2
- Move libparted libraries to /lib (#428420)

* Wed Jan 02 2008 David Cantrell <dcantrell@redhat.com> - 1.8.8-1
- Upgraded to GNU parted-1.8.8
- License for GNU parted is now GPLv3+

* Thu Dec 13 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-13
- Modify parted man page to indicate which flags are valid for which
  disk labels (#242711)

* Mon Nov 05 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-12
- Add KNOWN ISSUES section to parted(8) man page explaining that we cannot
  currently do ext3 resizing inside parted (#367101)
- Update the xvd patch to include 'xvd' in the string table that parted
  uses when printing device types (#366971)
- Do not install the linux.h or gnu.h headers

* Tue Oct 30 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-11
- Do not install fdasd.h and vtoc.h header files

* Thu Oct 04 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-10
- Do not install the testsuite tools

* Thu Oct 04 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-9
- Always define PED_DEVICE_DM regardless of compile time options

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-8
- Rebuild

* Wed Aug 08 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-7
- Update License tag to GPLv2+

* Tue Aug 07 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-6
- Detect Xen virtual block devices and set model name appropriately

* Thu Apr 19 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-5
- Spec file cleanups for merge review (#226230)

* Fri Apr 13 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-4
- Fix primary partition cylinder alignment error for DOS disk labels (#229745)
- Do not build and package up libparted.a, only the shared library

* Wed Apr 11 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-3
- Fix off-by-one bug in parted(8) when displaying disk label (#235901)

* Wed Mar 21 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-2
- Do not translate partition name from disk label (#224182)

* Tue Mar 20 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-1
- Upgrade to GNU parted-1.8.6, summary of major change(s):
     a) Revert linux-swap(new) and linux-swap(old) fs types, it's
        linux-swap for all swap types (#233085)

* Tue Mar 20 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-1
- Upgrade to GNU parted-1.8.5 (added missing po files)

* Fri Mar 16 2007 David Cantrell <dcantrell@redhat.com> - 1.8.4-1
- Upgrade to GNU parted-1.8.4, summary of major changes:
     a) Update to use newest GNU developer tools
     b) Use gnulib, the GNU portability library
     c) HFS+ resize support
     d) Windows Vista fixes
     e) AIX disk label fixes
     f) >512 byte logical sector read support on Linux
- Spec file cleanups per Fedora packaging guidelines

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 1.8.2-5
- Remove period from end of summary line (package review)
- Use preferred BuildRoot (package review)
- BR device-mapper-devel

* Tue Jan 30 2007 David Cantrell <dcantrell@redhat.com> - 1.8.2-4
- Patched parted.8 man page to show partition names apply to GPT disklabels
  as well as Mac and PC98 disklabels (#221600)

* Mon Jan 22 2007 David Cantrell <dcantrell@redhat.com> - 1.8.2-3
- Remove BR for libtermcap-devel
- Specifically preserve starting alignment of 0x800 on Windows Vista
  (see http://support.microsoft.com/kb/923332 for details)
- Fix incorrect sector parameter used to initialize a new PedAlignment

* Thu Jan 18 2007 David Cantrell <dcantrell@redhat.com> - 1.8.2-2
- Preserve starting sector for primary NTFS 3.1 partitions (Windows
  Vista) when modifying the DOS disk label.  NTFS 3.1 partitions do
  not start on the 2nd head of the 1st cylinder at the beginning of
  the drive.

* Fri Jan 12 2007 David Cantrell <dcantrell@redhat.com> - 1.8.2-1
- Upgrade to GNU parted-1.8.2

* Fri Dec 15 2006 David Cantrell <dcantrell@redhat.com> - 1.8.1-2
- Fix a segfault when initializing new volumes (pjones)

* Mon Dec 04 2006 David Cantrell <dcantrell@redhat.com> - 1.8.1-1
- Upgrade to GNU parted-1.8.1

* Fri Nov 17 2006 David Cantrell <dcantrell@redhat.com> - 1.8.0-1
- Upgrade to GNU parted-1.8.0

* Thu Nov 02 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-18
- Detect Apple_Boot partition types correctly (#204714)

* Thu Oct 26 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-17
- For init_generic() failures on user-mode Linux block devices, goto
  error_free_arch_specific instead of error_free_dev.

* Wed Oct 04 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-16
- Don't throw PED_EXCEPTION_ERROR in ped_geometry_read() if accessing
  sectors outside of partition boundary, since returning false will
  shift ped_geometry_check() to the correct sectors.

* Wed Aug 23 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-15
- Fixed gpt patch (*asked_already -> asked_already, whoops)

* Tue Aug 22 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-14
- Improve error message returned by _parse_header() on GPT-labeled disks
  so users actually have an idea of how to correct the problem
- Fix off-by-one error with LastUsableLBA and PartitionEntryLBA overlap
  to prevent possible data corruption when using non-parted GPT editing
  tools

* Mon Aug 21 2006 Peter Jones <pjones@redhat.com> - 1.7.1-13
- Don't use the "volume name" as the device node name on dm device
  partitions, it isn't really what we want at all.

* Thu Aug 17 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-12
- Updated O_DIRECT patch to work around s390 problems
- Update LastUsableLBA on GPT-labeled disks after LUN resize (#194238)
- Fix exception when backup GPT table is not in the correction location
  and parted tries to move it (#194238)

* Tue Aug 15 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-11
- Expand error buffer to 8192 bytes in vtoc_error()
- Do not apply O_DIRECT patch on S/390 or S/390x platforms

* Mon Aug 14 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-10
- Removed bad header file patch (#200577)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7.1-9.1
- rebuild

* Wed Jul  5 2006 Peter Jones <pjones@redhat.com> - 1.7.1-9
- add ped_exception_get_handler()

* Mon Jun 26 2006 Florian La Roche <laroche@redhat.com> - 1.7.1-8
- remove info files in preun

* Thu Jun 22 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-7
- PED_SECTOR_SIZE -> PED_SECTOR_SIZE_DEFAULT

* Thu Jun 22 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-6
- Roll dasd patches together
- Use O_DIRECT to prevent first partition corruption on GPT disks

* Thu Jun 15 2006 Jeremy Katz <katzj@redhat.com> - 1.7.1-5
- fix segfaults with dasd devices

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.7.1-4
- move .so symlink to -devel subpackage

* Sun May 28 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-3
- Rebuild

* Sun May 28 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-2
- Removed mac-swraid patch (added upstream)
- Updated device-mapper patch for parted-1.7.1

* Sat May 27 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-1
- Upgraded to parted-1.7.1

* Fri May 19 2006 David Cantrell <dcantrell@redhat.com> - 1.7.0-1
- Upgraded to parted-1.7.0

* Thu Apr 13 2006 David Cantrell <dcantrell@redhat.com> - 1.6.25.1-1
- Upgraded to parted-1.6.25.1
- BuildRequires libtool

* Tue Mar 14 2006 Jeremy Katz <katzj@redhat.com> - 1.6.25-8
- fix ppc swraid
- BR gettext-devel

* Wed Feb 22 2006 Peter Jones <pjones@redhat.com> - 1.6.25-7
- close /proc/devices correctly

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.6.25-6.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Peter Jones <pjones@redhat.com> 1.6.25-6
- Fix dm partition naming.

* Tue Feb  7 2006 Jesse Keating <jkeating@redhat.com> 1.6.25-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec  9 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Peter Jones <pjones@redhat.com> 1.6.25-5
- rebuild for new device-mapper

* Thu Dec  1 2005 Peter Jones <pjones@redhat.com> 1.6.25-4
- change device-mapper code to call dm_task_update_nodes() after
  tasks which change device nodes.

* Wed Nov 16 2005 Peter Jones <pjones@redhat.com> 1.6.25-3
- fix /proc/devices parser bug

* Tue Nov 15 2005 Peter Jones <pjones@redhat.com> 1.6.25-2
- add support for partitions on dm devices

* Wed Nov 09 2005 Chris Lumens <clumens@redhat.com> 1.6.25-1
- Updated to 1.6.25.
- Update DASD, iseries, and SX8 patches.

* Tue Aug 30 2005 Chris Lumens <clumens@redhat.com> 1.6.24-1
- Updated to 1.6.24.

* Mon Jul 18 2005 Chris Lumens <clumens@redhat.com> 1.6.23-2
- Add buildreq for texinfo.

* Fri Jul 08 2005 Chris Lumens <clumens@redhat.com> 1.6.23-1
- Updated to 1.6.23.
- Get rid of separate Mac patches that are now included in upstream.
- Update DASD and AIX patches.

* Tue Jun 07 2005 Chris Lumens <clumens@redhat.com> 1.6.22-3
- Modified Apple_Free patch to take care of the case where the partitions
  are unnamed, causing many errors to be printed (#159047).

* Thu May 05 2005 Chris Lumens <clumens@redhat.com> 1.6.22-2
- Added upstream patch to display certain Apple_Free partitions (#154479).

* Wed Mar 23 2005 Chris Lumens <clumens@redhat.com> 1.6.22-1
- Updated to 1.6.22.
- Get rid of separate gc4 patch that's now included upstream.
- Take Mac LVM patch from parted CVS.

* Mon Mar 14 2005 Chris Lumens <clumens@redhat.com> 1.6.21-3
- Include patches from parted CVS for new gcc4 warnings.

* Sun Feb 20 2005 Paul Nasrat <pnasrat@redhat.com> 1.6.21-2
- Support lvm flags on mac partitions (#121266)

* Fri Jan 21 2005 Chris Lumens <clumens@redhat.com> 1.6.21-1 
- Updated to 1.6.21

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 1.6.20-2
- Rebuilt for new readline.

* Fri Jan 07 2005 Chris Lumens <clumens@redhat.com> 1.6.20-1 
- Updated to 1.6.20 (#139257, #142100).
- Updated DASD and AIX patches for 1.6.20.

* Tue Dec 14 2004 Jeremy Katz <katzj@redhat.com> - 1.6.19-2
- add support for Promise SX8 devices

* Sun Nov 28 2004 Jeremy Katz <katzj@redhat.com> - 1.6.19-1
- update to 1.6.19 (#138419)

* Sun Nov 21 2004 Jeremy Katz <katzj@redhat.com> - 1.6.18-1
- update to 1.6.18

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.6.16-3
- Convert pt_BR-parted.8 to UTF-8

* Thu Nov 11 2004 Jeremy Katz <katzj@redhat.com> - 1.6.16-2
- add patch from Matt Domsch to fix consistency of GPT disk labels 
  with the EFI specification for disks > 2TB (#138480)
- understand the new Sun UFS partition ID
- merge the new geometry probing from CVS to see if that helps the 
  assertions people are seeing (#138419)

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 1.6.16-1
- update to 1.6.16
- rebuild for python 2.4

* Mon Oct 18 2004 Jeremy Katz <katzj@redhat.com> - 1.6.15-5
- add patch from Matt Domsch to add a unique signature to new DOS labels 
  so that we can later determine which BIOS disk is which (#106674)

* Fri Oct 15 2004 Phil Knirsch <pknirsch@redhat.com> 1.6.15-4
- Fixed dasd patch (had some duplicate file patches in it)
- Fixed problem with parted segfaulting on SCSI discs on s390 (#133997)

* Tue Oct 12 2004 Jeremy Katz <katzj@redhat.com> - 1.6.15-3
- add patch from peterm to fix printing of the size of large devices (#135468)

* Thu Oct 07 2004 Phil Knirsch <pknirsch@redhat.com> 1.6.15-2
- Fixed geometry calculation for bios_geo in dasd_init()

* Mon Sep 20 2004 Jeremy Katz <katzj@redhat.com> - 1.6.15-1
- 1.6.15

* Fri Sep 10 2004 Jeremy Katz <katzj@redhat.com> - 1.6.14-1
- update to 1.6.14

* Tue Aug 24 2004 Jeremy Katz <katzj@redhat.com> - 1.6.12-2
- fix assertion error when checking flags on non-active partition (#130692)
- buildrequires: gettext-devel

* Mon Aug 16 2004 Jeremy Katz <katzj@redhat.com> - 1.6.12-1
- update to 1.6.12 with major changes to CHS handling to hopefully fix #115980
- adjust dasd patch accordingly, drop some included patches

* Mon Jul 19 2004 Karsten Hopp <karsten@redhat.de> 1.6.11-4 
- update dasd patch for dos-type partitions on mainframes (scsi disks)

* Fri Jun 25 2004 Jeremy Katz <katzj@redhat.com> - 1.6.11-3
- install-info (#77687)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> - 1.6.11-2
- rebuilt

* Tue Jun  1 2004 Jeremy Katz <katzj@redhat.com>
- -devel requires main package (#124938)

* Thu May 13 2004 Jeremy Katz <katzj@redhat.com> - 1.6.11-1
- update to 1.6.11

* Tue May 11 2004 Jeremy Katz <katzj@redhat.com> - 1.6.9-4
- add patch from Matt Domsch to not use the get/set last sector ioctls 
  with a 2.6 kernel (#121455)

* Thu Apr 15 2004 David Woodhouse <dwmw2@redhat.com> - 1.6.9-3
- Fix Mac partition detection to close #112937

* Tue Apr 13 2004 Jeremy Katz <katzj@redhat.com> - 1.6.9-2
- another minor tweak for 2.6's lack of sane geometry handling

* Mon Apr 12 2004 Jeremy Katz <katzj@redhat.com> - 1.6.9-1
- update to 1.6.9
- need automake17
- python-devel is superfluous with pyparted as a separate package
- lose the fake-libtool stuff, 1.6.9 was disted with newer auto*

* Mon Mar 15 2004 Elliot Lee <sopwith@redhat.com> 1.6.6-2
- Fix parted's "part-static" option to close #118183. Woohoo, a fake-libtool.sh :)

* Fri Mar 12 2004 Jeremy Katz <katzj@redhat.com> - 1.6.6-1
- update to 1.6.6 
- split dasd into a patch instead of included in the tarball
- python module is now in the pyparted package (separate src.rpm)
- ExcludeArch: ppc64 (#118183)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  6 2004 Jeremy Katz <katzj@redhat.com>
- add automake buildrequires (#115063)

* Thu Jan 22 2004 Jeremy Katz <katzj@redhat.com> 1.6.3-33
- 2.6 removes the geometry fixups that used to be present for IDE disks.  
  According to Andries, just follow what's in the partition table and don't 
  worry about what Linux "detects"

* Thu Nov  6 2003 Jeremy Katz <katzj@redhat.com> 1.6.3-32
- rebuild for python 2.3

* Mon Oct 27 2003 Jeremy Katz <katzj@redhat.com> 1.6.3-31
- add patch from Michael Schwendt <mschwendt@users.sf.net> for segfault

* Wed Sep 17 2003 Jeremy Katz <katzj@redhat.com> 1.6.3-30
- rebuild

* Wed Sep 17 2003 Jeremy Katz <katzj@redhat.com> 1.6.3-29
- and don't barf on the old (broken) 1.02 gpt rev

* Tue Sep 16 2003 Jeremy Katz <katzj@redhat.com> 1.6.3-28
- rebuild

* Tue Sep 16 2003 Jeremy Katz <katzj@redhat.com> 1.6.3-27
- write out the correct gpt revision (#103664)
- add buildrequires on ncurses-devel

* Thu Sep  4 2003 Bill Nottingham <notting@redhat.com> 1.6.3-26
- rebuild 

* Thu Sep  4 2003 Bill Nottingham <notting@redhat.com> 1.6.3-25
- don't buildreq libunicode-devel

* Thu Aug 07 2003 Elliot Lee <sopwith@redhat.com> 1.6.3-24
- Fix libtool

* Wed Jul 09 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-23
- Fixed dasd_write and dasd_read to support lvm and raid partitions.

* Wed Jun 18 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-22
- Fixed a small bug in VTOC fdasd_check_volume() (#97300).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 1.6.3-21
- rebuilt

* Wed Jun  4 2003 Matt Wilson <msw@redhat.com> 1.6.3-20
- don't detect AIX physical volumes as msdos partition tables (#91748)
- added stubbed code for manipulating AIX PVs, enough to clobber the
  signature. (#91748)

* Wed Jun 04 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-19
- Added LDL disk layout support for s390(x).

* Sun May 18 2003 Matt Wilson <msw@redhat.com> 1.6.3-18
- use metadata partitions to protect DASD VTOC
- stash DASD specific data in disk specific areas, not arch specific
  areas.

* Fri May 16 2003 Matt Wilson <msw@redhat.com> 1.6.3-18
- recongnize iseries viodasd (#90449)

* Thu May 08 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-17
- Fixed problem with probing partitions on s390(x) with new partition code.

* Mon May 05 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-16
- Fixed partiton reread code for s390(x).

* Fri May 02 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-15
- Rewrote partition handling for s390(x) dasd devices. No more empty partitions.

* Wed Mar 12 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-13
- Finished updating vtoc and fdasd code to latest s390-utils version.

* Thu Mar 06 2003 Phil Knirsch <pknirsch@redhat.com> 1.6.3-12
- Fixed vtoc handling on s390(x) dasd devices.

* Thu Feb 06 2003 Karsten Hopp <karsten@redhat.de> 1.6.3-11
- use different define to enable DASD debugging
  Otherwise we'll get a lot of dasd debug output because DEBUG is
  always defined

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Karsten Hopp <karsten@redhat.de> 1.6.3-9
- missed one debug message

* Tue Jan 21 2003 Karsten Hopp <karsten@redhat.de> 1.6.3-8
- add patch from CVS to disable debug messages on s390

* Tue Jan 14 2003 Matt Wilson <msw@redhat.com> 1.6.3-7
- updated to a new tarball of parted that includes a fs.probe_specific binding

* Sun Dec  1 2002 Matt Wilson <msw@redhat.com> 1.6.3-6
- hack in partition.native_type (#78118)

* Thu Nov  7 2002 Matt Wilson <msw@redhat.com>
- added a patch to avoid SIGFPE when fat sector size is 0

* Tue Nov  5 2002 Matt Wilson <msw@redhat.com>
- use --disable-dynamic-loading

* Mon Nov  4 2002 Matt Wilson <msw@redhat.com>
- add device.disk_new_fresh()

* Fri Nov  1 2002 Matt Wilson <msw@redhat.com>
- 1.6.3

* Fri Oct  4 2002 Jeremy Katz <katzj@redhat.com> 1.4.24-7
- use make LIBTOOL=/usr/bin/libtool instead of recreating everything
- add patch from Jack Howarth <howarth@bromo.med.uc.edu> to self host properly
- add patch to treat GPT structs as little-endian always and treat GUIDS 
  as little-endian blobs
- add patch to recognize hp service partitions

* Wed Sep 25 2002 Jeremy Katz <katzj@redhat.com> 1.4.24-6hammer
- libtoolize, etc for x86_64
- hack to get the python module in the right place until python.m4 
  from automake is fixed

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.4.24-6
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 1.4.24-5
- automated rebuild

* Wed May 22 2002 Jeremy Katz <katzj@redhat.com> 1.4.24-4
- rebuild in new environment

* Fri Mar 22 2002 Matt Wilson <msw@redhat.com> 1.4.24-3
- fixed the probe-with-open behavior (again)

* Fri Feb 22 2002 Matt Wilson <msw@redhat.com> 1.4.24-1
- rebuild

* Tue Feb 12 2002 Matt Wilson <msw@redhat.com> 1.4.24-1
- 1.4.24

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan  7 2002 Jeremy Katz <katzj@redhat.com> 1.4.20-4
- build with final python 2.2

* Wed Dec 12 2001 Jeremy Katz <katzj@redhat.com> 1.4.20-3
- update from CVS and rebuild in new environment

* Thu Oct 25 2001 Jeremy Katz <katzj@redhat.com> 1.4.20-2
- build both python1.5 and python2 modules

* Fri Oct 19 2001 Matt Wilson <msw@redhat.com> 1.4.20-1
- 1.4.20 final

* Thu Oct 11 2001 Matt Wilson <msw@redhat.com> 1.4.20-0.1pre3
- new dist from CVS with new autoconf and automake
- gpt is in 1.4.20, removed patch1 (gpt support)
- partstatic is in 1.4.20, removed patch2 (partstatic patch)

* Tue Aug 28 2001 Matt Wilson <msw@redhat.com> 1.4.16-8
- new dist from cvs with changes to the python binding: register
  DEVICE_I20 and DEVICE_ATARAID, check to make sure that a partition
  exists in the PedDisk when using it to find ped_disk_next_partition

* Tue Aug 21 2001 Matt Wilson <msw@redhat.com> 1.4.16-7
- really disable pc98 support (SF #51632)

* Fri Aug 17 2001 Matt Wilson <msw@redhat.com> 1.4.16-6
- added a patch (Patch1) to link the c library in dynamically, the
  rest of the libs statically for the parted binary (MF #49358)

* Tue Aug  7 2001 Matt Wilson <msw@redhat.com>
- made a new dist from CVS that includes binding for
  disk.get_partition_by_sector and accessing the name of a disk type

* Mon Aug  6 2001 Matt Wilson <msw@redhat.com> 1.4.16-4
- created a new dist from CVS that fixes ext3 detection when
  _probe_with_open is needed (#50292)

* Fri Jul 20 2001 Matt Wilson <msw@redhat.com>
- rewrite scsi id code (#49533)

* Fri Jul 20 2001 Matt Wilson <msw@redhat.com>
- added build requires (#49549)

* Tue Jul 17 2001 Matt Wilson <msw@redhat.com>
- 1.4.16
- regenerated gpt patch against 1.4.16, incorporated
  parted-1.4.15-pre1-gpt-printf.patch into the same patch, removed Patch1

* Tue Jul 10 2001 Matt Wilson <msw@redhat.com>
- added a new dist tarball that contains python wrappers to get disk types

* Tue Jul 10 2001 Tim Powers <timp@redhat.com>
- run ldconfig on un/install

* Tue Jul 10 2001 Matt Wilson <msw@redhat.com>
- added a fix from clausen for border case when there is an extended
  on the last cyl

* Mon Jul  9 2001 Matt Wilson <msw@redhat.com>
- 1.4.15

* Thu Jul  5 2001 Matt Wilson <msw@redhat.com>
- added patch from Arjan to enable ataraid support

* Wed Jul  4 2001 Matt Wilson <msw@redhat.com>
- imported 1.4.15-pre2 into CVS and made a new dist tarball

* Tue Jun 26 2001 Matt Wilson <msw@redhat.com>
- added a new dist tarball that contains a check in python code to
  make sure that a partition exists within a disk before trying to
  remove it from the disk
- also changed _probe_with_open to make the first probed filesystem win

* Tue Jun 26 2001 Bill Nottingham <notting@redhat.com>
- fix filesystem type reading on GPT disks

* Tue Jun 26 2001 Matt Wilson <msw@redhat.com>
- added another fix for ext2/ext3
- added Patch4 to move the crc32 function into its own namespace so
  we don't colide with zlib when both are in the same executable space

* Mon Jun 25 2001 Matt Wilson <msw@redhat.com>
- added a new dist tarball from CVS that includes
  ext3 probing

* Wed Jun  6 2001 Matt Wilson <msw@redhat.com>
- updated dist with binding for partition.geom.disk

* Tue Jun  5 2001 Matt Wilson <msw@redhat.com>
- make a new dist tarball that has new python binding changes

* Tue May 29 2001 Bill Nottingham <notting@redhat.com>
- add major numbers for cciss 
- add libunicode-devel buildprereq

* Sun May 27 2001 Matthew Wilson <msw@redhat.com>
- added type, heads, and sectors to the python binding for PedDevice

* Fri May  4 2001 Matt Wilson <msw@redhat.com>
- added parted-1.4.11-gpt-pmbralign.patch from Matt Domsch

* Wed May  2 2001 Matt Wilson <msw@redhat.com>
- include python binding
- enable shared library (for python binding, we want fpic code)
  with --enable-shared
- build parted binary static with --enable-all-static
- don't run libtoolize on this.

* Wed May 02 2001 Bill Nottingham <notting@redhat.com>
- update to 1.4.11
- add EFI GPT patch from Matt Domsch (<Matt_Domsch@dell.com>)
- don't run autoconf, it relies on a newer non-released version
  of autoconf...

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify

* Wed Jan 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.4.7

* Thu Dec 14 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Fri Nov 03 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.12

* Wed Nov 01 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.11

* Tue Oct 17 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.10

* Sun Sep 10 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.9

* Tue Aug 29 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix bug when just hitting "return" with no user input

* Sun Aug 20 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- 1.2.8
- blksize patch not needed anymore
- move changelog to the end of the spec file

* Wed Aug 16 2000 Matt Wilson <msw@redhat.com>
- 1.2.7
- patched configure script to ignore the 2.4 blkpg.h header (fixes #15835).

* Fri Aug  4 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.6

* Sat Jul 22 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.2.5
- add more docu

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Matt Wilson <msw@redhat.com>
- initialization of spec file.
