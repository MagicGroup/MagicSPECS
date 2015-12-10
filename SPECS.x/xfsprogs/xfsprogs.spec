Summary:	Utilities for managing the XFS filesystem
Summary(zh_CN.UTF-8): 管理 XFS 文件系统的工具
Name:		xfsprogs
Version:	4.2.0
Release:	4%{?dist}
# Licensing based on generic "GNU GENERAL PUBLIC LICENSE"
# in source, with no mention of version.
# doc/COPYING file specifies what is GPL and what is LGPL
# but no mention of versions in the source.
License:	GPL+ and LGPLv2+
Group:		System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/cmd_tars/%{name}-%{version}.tar.gz
Source1:	xfsprogs-wrapper.h
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool, gettext, libuuid-devel
BuildRequires:	readline-devel, libblkid-devel >= 2.17-0.1.git5e51568
Provides:	xfs-cmds
Obsoletes:	xfs-cmds <= %{version}
Conflicts:	xfsdump < 3.0.1

%description
A set of commands to use the XFS filesystem, including mkfs.xfs.

XFS is a high performance journaling filesystem which originated
on the SGI IRIX platform.  It is completely multi-threaded, can
support large files and large filesystems, extended attributes,
variable block sizes, is extent based, and makes extensive use of
Btrees (directories, extents, free space) to aid both performance
and scalability.

Refer to the documentation at http://oss.sgi.com/projects/xfs/
for complete details.  This implementation is on-disk compatible
with the IRIX version of XFS.

%description -l zh_CN.UTF-8
管理 XFS 文件系统的工具。

%package devel
Summary: XFS filesystem-specific headers
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: xfsprogs = %{version}-%{release}, libuuid-devel

%description devel
xfsprogs-devel contains the header files needed to develop XFS
filesystem-specific programs.

You should install xfsprogs-devel if you want to develop XFS
filesystem-specific programs,  If you install xfsprogs-devel, you'll
also want to install xfsprogs.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
export tagname=CC
%configure \
        --enable-readline=yes	\
	--enable-blkid=yes

# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make V=1 DIST_ROOT=$RPM_BUILD_ROOT install install-dev \
	PKG_ROOT_SBIN_DIR=%{_sbindir} PKG_ROOT_LIB_DIR=%{_libdir}

# nuke .la files, etc
rm -f $RPM_BUILD_ROOT/{%{_lib}/*.{la,a,so},%{_libdir}/*.{la,a}}
chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/libhandle.so.*.*.*

# remove non-versioned docs location
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/xfsprogs/
magic_rpm_clean.sh
%find_lang %{name} || :

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc doc/CHANGES doc/COPYING doc/CREDITS README
%{_libdir}/*.so.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_mandir}/man3/*
%dir %{_includedir}/xfs
%{_includedir}/xfs/handle.h
%{_includedir}/xfs/jdm.h
%{_includedir}/xfs/linux.h
%{_includedir}/xfs/xfs.h
%{_includedir}/xfs/xfs_arch.h
%{_includedir}/xfs/xfs_fs.h
%{_includedir}/xfs/xfs_types.h
%{_includedir}/xfs/xfs_format.h
%{_includedir}/xfs/xfs_da_format.h
%{_includedir}/xfs/xfs_log_format.h
%{_includedir}/xfs/xqm.h

%{_libdir}/*.so

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 4.2.0-4
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 4.2.0-3
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.2.0-2
- 更新到 4.2.0

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.1.8-5
- 为 Magic 3.0 重建

* Fri Mar 30 2012 Eric Sandeen <sandeen@redhat.com> 3.1.8-4
- Rebuild against new RPM (RHBZ#808250)

* Wed Mar 28 2012 Eric Sandeen <sandeen@redhat.com> 3.1.8-3
- Move files out of /lib64 to /usr/lib64

* Wed Mar 28 2012 Eric Sandeen <sandeen@redhat.com> 3.1.8-2
- Move files out of /sbin to /usr/sbin

* Fri Mar 23 2012 Eric Sandeen <sandeen@redhat.com> 3.1.8-1
- New upstream release.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Eric Sandeen <sandeen@redhat.com> 3.1.7-1
- New upstream release.

* Mon Oct 17 2011 Eric Sandeen <sandeen@redhat.com> 3.1.6-2
- Remove mistaken "test" in release string

* Fri Oct 14 2011 Eric Sandeen <sandeen@redhat.com> 3.1.6-1.test
- New upstream release.  Drop -DNDEBUG build flag.

* Thu Mar 31 2011 Eric Sandeen <sandeen@redhat.com> 3.1.5-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Eric Sandeen <sandeen@redhat.com> 3.1.4-1
- New upstream release; disable DEBUG for now to build

* Sat Aug 28 2010 Eric Sandeen <sandeen@redhat.com> 3.1.3-1
- New upstream release

* Fri May 07 2010 Eric Sandeen <sandeen@redhat.com> 3.1.2-1
- New upstream release

* Thu Apr 01 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-7
- make devel pkg require libuuid-devel (#576296)

* Mon Mar 15 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-6
- Fix missing locking for btree manipulation in xfs_repair

* Fri Feb 12 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-5
- --enable-static=no doesn't work; just nuke static libs

* Fri Feb 12 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-4
- Fix up -devel package descriptions

* Fri Feb 12 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-3
- Drop static libs (#556102)

* Mon Feb 01 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-2
- Fix mkfs of target with nothing blkid can recognize (#561870)
 
* Mon Feb 01 2010 Eric Sandeen <sandeen@redhat.com> 3.1.1-1
- New upstream release
- Fix fd validity test for device-less mkfs invocation
 
* Sun Jan 17 2010 Eric Sandeen <sandeen@redhat.com> 3.1.0-2
- Post-release mkfs fixes (#555847)

* Wed Jan 13 2010 Eric Sandeen <sandeen@redhat.com> 3.1.0-1
- New upstream release
- Minor fixups for new glibc headers
- Fixes default mkfs.xfs on 4k sector device (#539553)

* Tue Dec 08 2009 Eric Sandeen <sandeen@redhat.com> 3.0.3-5
- And finally, BuildRequire libblkid-devel

* Mon Dec 07 2009 Eric Sandeen <sandeen@redhat.com> 3.0.3-4
- Actually patch & run configure script w/ blkid bits...
- Kill rpath in xfs_fsr

* Fri Nov 20 2009 Eric Sandeen <sandeen@redhat.com> 3.0.3-3
- Fix up build issues w.r.t. off64_t

* Tue Nov 10 2009 Eric Sandeen <sandeen@redhat.com> 3.0.3-2
- Add trim/discard & libblkid support

* Tue Sep 01 2009 Eric Sandeen <sandeen@redhat.com> 3.0.3-1
- New upstream release

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-9
- Fix block overflows in xfs_repair and xfs_metadump

* Tue Jun 30 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-8
- Fix up build-requires after e2fsprogs splitup

* Thu Jun 18 2009 Dennis Gilmore <dennis@ausil.us> 3.0.1-7
- update sparc multilib handling

* Mon Jun 15 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-6
- Make lazy superblock counters the default

* Mon Jun 15 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-5
- Add fallocate command to config script & fix for 32-bit

* Mon Jun 15 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-4
- Add fallocate command to xfs_io

* Fri May 15 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-3
- Fix and re-enable readline

* Tue May 05 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-2
- Conflict with xfsdump < 3.0.1 since files moved between them

* Tue May 05 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-1
- New upstream release

* Sat Apr 18 2009 Eric Sandeen <sandeen@redhat.com> 3.0.0-4
- Fix build for non-multilib arches, oops.

* Sat Apr 18 2009 Eric Sandeen <sandeen@redhat.com> 3.0.0-3
- Create new xfsprogs-qa-devel subpackage

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Eric Sandeen <sandeen@redhat.com> 3.0.0-1
- New upstream release

* Thu Jan 08 2009 Eric Sandeen <sandeen@redhat.com> 2.10.2-3
- Fix perms of libhandle.so in specfile, not makefile

* Wed Jan 07 2009 Eric Sandeen <sandeen@redhat.com> 2.10.2-2
- Fix perms of libhandle.so so that it's properly stripped

* Sun Dec 07 2008 Eric Sandeen <sandeen@redhat.com> 2.10.2-1
- New upstream release, bugfix only.

* Wed Nov 26 2008 Eric Sandeen <sandeen@redhat.com> 2.10.1-4
- Add protection from borken sys_ustat
- Add final upstream versions of gfs2 & parallel build patches

* Wed Nov 12 2008 Eric Sandeen <sandeen@redhat.com> 2.10.1-2
- Recognize gfs/gfs2 in libdisk
- Enable parallel builds

* Fri Sep 05 2008 Eric Sandeen <sandeen@redhat.com> 2.10.1-1
- Update to xfsprogs 2.10.1
- Add ASCII case-insensitive support to xfsprogs.
- xfs_repair fixes

* Wed Jun 04 2008 Dennis Gilmore <dennis@ausil.us> 2.9.8-3
- sparc32 is built using the sparcv9 variant 

* Wed Jun 04 2008 Eric Sandeen <sandeen@redhat.com> 2.9.8-2
- Tidy up multilib hack for non-multilib arches & add sparc (#448452)

* Wed Apr 23 2008 Eric Sandeen <sandeen@redhat.com> 2.9.8-1
- Update to xfsprogs 2.9.8
- Add support for sb_features2 in wrong location
- Add -c option to xfs_admin to turn lazy-counters on/off
- Added support for mdp in libdisk/mkfs.xfs

* Sun Mar 02 2008 Eric Sandeen <sandeen@redhat.com> 2.9.7-1
- Update to xfsprogs 2.9.7
- Lazy sb counters back off by default; other misc fixes

* Wed Feb 06 2008 Eric Sandeen <sandeen@redhat.com> 2.9.6-1
- Update to xfsprogs 2.9.6 - fixes mkfs sizing problem.
- Trim down BuildRequires to what's actually required now

* Mon Jan 21 2008 Eric Sandeen <sandeen@redhat.com> 2.9.5-1
- Update to xfsprogs 2.9.5
- Contains more optimal mkfs defaults
- specfile cleanup, & don't restate config defaults

* Tue Oct 23 2007 Eric Sandeen <sandeen@redhat.com> 2.9.4-4
- Add arm to multilib header wrapper

* Tue Oct 02 2007 Eric Sandeen <sandeen@redhat.com> 2.9.4-3
- mkfs.xfs: Fix wiping old AG headers and purge whack buffers

* Mon Oct 01 2007 Eric Sandeen <sandeen@redhat.com> 2.9.4-2
- Add alpha to the multilib wrapper (#310411)

* Mon Sep 10 2007 Eric Sandeen <sandeen@redhat.com> 2.9.4-1
- Update to xfsprogs 2.9.4

* Fri Aug 24 2007 Eric Sandeen <sandeen@redhat.com> 2.9.3-3
- Add gawk to buildrequires

* Thu Aug 16 2007 Eric Sandeen <sandeen@redhat.com> 2.9.3-2
- Update license tag

* Thu Jul 26 2007 Eric Sandeen <sandeen@redhat.com> 2.9.3-1
- Upgrade to xfsprogs 2.9.2, quota, xfs_repair, and filestreams changes

* Thu Jul  6 2007 Eric Sandeen <sandeen@redhat.com> 2.8.21-1
- Upgrade to xfsprogs 2.8.21, lazy sb counters enabled,
  xfs_quota fix (#236746)

* Thu May 31 2007 Eric Sandeen <sandeen@redhat.com> 2.8.20-2
- Fix ppc64 build... again

* Fri May 25 2007 Eric Sandeen <sandeen@redhat.com> 2.8.20-1
- Upgrade to xfsprogs 2.8.20, several xfs_repair fixes

* Tue Mar 06 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.8.18-3
- Remove libtermcap-devel from BuildRequires

* Wed Feb 14 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.8.18-2
- Disable readline support for now (#223781)

* Sun Feb 04 2007 Jarod Wilson <jwilson@redhat.com> 2.8.18-1
- Post-facto changelog addition to note bump to 2.8.18

* Wed Sep 27 2006 Russell Cattelan <cattelan@thebarn.com> 2.8.11-3
- bump build version to 3 for a new brew build

* Tue Sep 26 2006 Russell Cattelan <cattelan@thebarn.com> 2.8.11-2
- add ppc64 build patch

* Thu Sep 21 2006 Russell Cattelan <cattelan@redhat.com> 2.8.11-1
- Upgrade to xfsprogs 2.8.11 Need to pick up important repair fixes

* Tue Jul 18 2006 Jeremy Katz <katzj@redhat.com> - 2.8.4-3
- exclude arch ppc64 for now (#199315)

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 2.8.4-2
- rebuild

* Tue Jul 04 2006 Robert Scheck <redhat@linuxnetz.de> 2.8.4-1
- Upgrade to 2.8.4 (#196599 #c2)

* Sun Jun 25 2006 Robert Scheck <redhat@linuxnetz.de> 2.8.3-1
- Upgrade to 2.8.3 (#196599)
- Applied Russell Coker's suggested patch to improve the
  performance for SELinux machines significantly (#120622)

* Sun Jun 25 2006 Robert Scheck <redhat@linuxnetz.de> 2.7.11-2
- Fixed multilib conflict of xfs/platform_defs.h (#192755)

* Sun Mar 12 2006 Robert Scheck <redhat@linuxnetz.de> 2.7.11-1
- Upgrade to 2.7.11 and spec file cleanup (#185234)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.7.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.7.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 31 2005 Robert Scheck <redhat@linuxnetz.de> 2.7.3-1
- Upgrade to 2.7.3 and enabled termcap support (#154323)

* Wed Sep 28 2005 Florian La Roche <laroche@redhat.com>
- fixup building with current rpm

* Wed Apr 20 2005 Dave Jones <davej@redhat.com>
- Disable debug. (#151438)
- Rebuild with gcc4

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> - 2.6.13-3
- Rebuilt for new readline.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  5 2004 Jeremy Katz <katzj@redhat.com> - 2.6.13-1
- update to 2.6.13 per request of upstream
- fixes mount by label of xfs on former raid partition (#122043)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan  8 2004 Jeremy Katz <katzj@redhat.com> 2.6.0-2
- add defattr (reported by Matthias)

* Tue Dec 23 2003 Elliot Lee <sopwith@redhat.com> 2.6.0-3
- Fix tyops in dependencies

* Mon Dec 22 2003 Jeremy Katz <katzj@redhat.com> 2.6.0-1
- build for Fedora Core
- switch to more explicit file lists, nuke .la files

* Tue Dec 16 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de> 2.6.0
- Update to 2.6.0.

* Sat Sep 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Sync with XFS 1.3.0.
- Update to 2.5.6.

* Thu Apr 10 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de> 2.3.9-0_2.90at
- Rebuilt for Red Hat 9.
