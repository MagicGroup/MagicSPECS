Name:          ceph
Version:	0.77
Release:       2%{?dist}
Summary:       User space components of the Ceph file system
License:       LGPLv2
Group:         System Environment/Base
URL:           https://ceph.com/

Source:        https://ceph.com/download/%{name}-%{version}.tar.bz2
Patch0:        ceph-init-fix.patch
# https://github.com/ceph/ceph/pull/1051
Patch1:        ceph-build-support-for-automake-1.12.patch
Patch2:        ceph-fix-sbin-target.patch

BuildRequires: fuse-devel, libtool, libtool-ltdl-devel, boost-devel,
BuildRequires: libedit-devel, fuse-devel, git, perl, gdbm, libaio-devel,
# google-perftools is not available on these:
%ifnarch ppc ppc64 s390 s390x aarch64 mips64el
BuildRequires: gperftools-devel
%endif
BuildRequires: cryptopp-devel, libatomic_ops-static, gcc-c++
BuildRequires: pkgconfig, libcurl-devel, keyutils-libs-devel
BuildRequires: gtkmm24-devel, gtk2-devel, libuuid, libuuid-devel
BuildRequires: leveldb-devel, snappy-devel, libblkid-devel

Requires(post): chkconfig, binutils, libedit
Requires(preun): chkconfig
Requires(preun): initscripts

%description
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability.

%package libs
Summary:       Ceph libraries
Group:         System Environment/Libraries
%description libs
Common libraries for Ceph distributed network file system

%package libcephfs
Summary:       Ceph libcephfs libraries
Group:         System Environment/Libraries
%description libcephfs
libcephfs library for Ceph distributed network file system

%package       fuse
Summary:       Ceph fuse-based client
Group:         System Environment/Base
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: fuse-devel
%description   fuse
FUSE based client for Ceph distributed network file system

%package     devel
Summary:     Ceph headers
Group:       Development/Libraries
License:     LGPLv2
Requires:    %{name}%{?_isa} = %{version}-%{release}
Requires:    %{name}-libs%{?_isa} = %{version}-%{release}
Requires:    %{name}-libcephfs%{?_isa} = %{version}-%{release}
%description devel
This package contains the headers needed to develop programs that use Ceph.

%package radosgw
Summary:        rados REST gateway
Group:          Development/Libraries
Requires:       mod_fcgid
BuildRequires:  fcgi-devel
BuildRequires:  expat-devel

%description radosgw
radosgw is an S3 HTTP REST gateway for the RADOS object store. It is
implemented as a FastCGI module using libfcgi, and can be used in
conjunction with any FastCGI capable web server.

%prep
%setup -q
%patch0 -p1 -b .init
%patch1 -p1
%patch2 -p1

%build
./autogen.sh

%ifarch armv5tel
# libatomic_ops does not have correct asm for ARMv5tel
EXTRA_CFLAGS="-DAO_USE_PTHREAD_DEFS"
%endif
%ifarch %{arm}
# libatomic_ops seems to fallback on some pthread implementation on ARM
EXTRA_LDFLAGS="-lpthread"
%endif

%{configure} --prefix=%{_prefix} --sbindir=%{_sbindir} \
--localstatedir=%{_localstatedir} --sysconfdir=%{_sysconfdir} \
%ifarch ppc ppc64 s390 s390x aarch64 mips64el
--without-tcmalloc \
%endif
--with-system-leveldb --without-hadoop --with-radosgw --with-gtk2 \
CFLAGS="$RPM_OPT_FLAGS $EXTRA_CFLAGS" \
CXXFLAGS="$RPM_OPT_FLAGS $EXTRA_CFLAGS -fvisibility-inlines-hidden" \
LDFLAGS="$EXTRA_LDFLAGS"

V=1 make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
install -D src/init-ceph $RPM_BUILD_ROOT%{_initrddir}/ceph
chmod 0644 $RPM_BUILD_ROOT%{_docdir}/ceph/sample.ceph.conf
rm -rf __tmp_docs ; mkdir __tmp_docs
mv $RPM_BUILD_ROOT%{_docdir}/ceph/* __tmp_docs
install -m 0644 -D src/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ceph
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/ceph/tmp/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ceph/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ceph/stat
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ceph
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d

%post
/sbin/chkconfig --add ceph

%preun
if [ $1 = 0 ] ; then
    /sbin/service ceph stop >/dev/null 2>&1
    /sbin/chkconfig --del ceph
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service ceph condrestart >/dev/null 2>&1 || :
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%post libcephfs -p /sbin/ldconfig
%postun libcephfs -p /sbin/ldconfig

%files
%doc README COPYING __tmp_docs/sample*
%dir %{_sysconfdir}/ceph
%{_bindir}/ceph
%{_bindir}/cephfs
%{_bindir}/ceph-conf
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-crush-location
%{_bindir}/ceph_filestore_tool
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-authtool
%{_bindir}/ceph-syn
%{_bindir}/ceph-run
%{_bindir}/ceph-mon
%{_bindir}/ceph-mds
%{_bindir}/ceph-osd
%{_bindir}/ceph-rbdnamer
%{_bindir}/rados
%{_bindir}/rbd
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-coverage
%{_bindir}/ceph-dencoder
%{_bindir}/ceph_filestore_dump
%{_bindir}/ceph_mon_store_converter
%{_bindir}/ceph-post-file
%{_bindir}/ceph-rest-api
%{_initrddir}/ceph
%{_sbindir}/mkcephfs
%{_sbindir}/mount.ceph
%{_sbindir}/ceph-disk-activate
%{_sbindir}/ceph-disk-prepare
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk
%{_sbindir}/ceph-disk-udev
%{_libdir}/ceph
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rados
%config(noreplace) %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rbd
%{_mandir}/man8/ceph-mon.8*
%{_mandir}/man8/ceph-mds.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/mkcephfs.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/cephfs.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-debugpack.8*
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-rest-api.8*
%{_mandir}/man8/ceph-post-file.8*
%{python_sitelib}/rados.py*
%{python_sitelib}/rbd.py*
%{python_sitelib}/cephfs.py*
%{python_sitelib}/ceph_argparse.py*
%{python_sitelib}/ceph_rest_api.py*
%dir %{_localstatedir}/lib/ceph/
%dir %{_localstatedir}/lib/ceph/tmp/
%dir %{_localstatedir}/log/ceph/
%{_datadir}/ceph/id_dsa_drop.ceph.com*
%{_datadir}/ceph/known_hosts_drop.ceph.com

%files libs
%doc COPYING
%{_libdir}/librados.so.*
%{_libdir}/librbd.so.*
%{_libdir}/rados-classes/libcls_user.so.*
%if 0
%dir %{_libdir}/erasure-code
# Warning to future maintainers: Note that the libec_ and libcls_ unversioned
# shared objects are included here in the libs subpackage. These files are
# plugins that Ceph loads with dlopen(). They belong here in -libs, not
# -devel.
%{_libdir}/erasure-code/libec_example.so*
%{_libdir}/erasure-code/libec_fail_to_initialize.so*
%{_libdir}/erasure-code/libec_fail_to_register.so*
%{_libdir}/erasure-code/libec_hangs.so*
%{_libdir}/erasure-code/libec_jerasure.so*
%{_libdir}/erasure-code/libec_missing_entry_point.so*
%endif
%dir %{_libdir}/rados-classes
# See warning note above about unversioned shared objects here. These belong
# here in -libs (not -devel).
%{_libdir}/rados-classes/libcls_hello.so*
%{_libdir}/rados-classes/libcls_rbd.so*
%{_libdir}/rados-classes/libcls_rgw.so*
%{_libdir}/rados-classes/libcls_lock.so*
%{_libdir}/rados-classes/libcls_kvs.so*
%{_libdir}/rados-classes/libcls_refcount.so*
%{_libdir}/rados-classes/libcls_log.so*
%{_libdir}/rados-classes/libcls_replica_log.so*
%{_libdir}/rados-classes/libcls_statelog.so*
%{_libdir}/rados-classes/libcls_version.so*

%files libcephfs
%doc COPYING
%{_libdir}/libcephfs.so.*

%files fuse
%doc COPYING
%{_bindir}/ceph-fuse
%{_bindir}/rbd-fuse
%{_sbindir}/mount.fuse.ceph
%{_mandir}/man8/ceph-fuse.8*
%{_mandir}/man8/rbd-fuse.8*

%files devel
%doc COPYING
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/rados_types.hpp
%{_includedir}/rados/buffer.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/libcephfs.so
%{_libdir}/librados.so
%{_libdir}/librbd.so
%{_bindir}/librados-config
%{_mandir}/man8/librados-config.8*
%{_includedir}/rados/memory.h
%{_libdir}/rados-classes/libcls_user.so

%files radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
%{_sysconfdir}/bash_completion.d/radosgw-admin

%changelog
* Sat Mar 08 2014 Liu Di <liudidi@gmail.com> - 0.77-2
- 更新到 0.77

* Thu Feb 06 2014 Ken Dreyer <ken.dreyer@inktank.com> - 0.72.2-2
- Move plugins from -devel into -libs package (#891993). Thanks Michael
  Schwendt.

* Mon Jan 06 2014 Ken Dreyer <ken.dreyer@inktank.com> 0.72.2-1
- Update to latest stable upstream release
- Use HTTPS for URLs
- Submit Automake 1.12 patch upstream
- Move unversioned shared libs from ceph-libs into ceph-devel

* Wed Dec 18 2013 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> 0.67.3-4
- build without tcmalloc on aarch64 (no gperftools)

* Sat Nov 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.67.3-3
- gperftools not currently available on aarch64

* Mon Oct 07 2013 Dan Horák <dan[at]danny.cz> - 0.67.3-2
- fix build on non-x86_64 64-bit arches

* Wed Sep 11 2013 Josef Bacik <josef@toxicpanda.com> - 0.67.3-1
- update to 0.67.3

* Wed Sep 11 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 0.61.7-3
- let base package include all its documentation files via %%doc magic,
  so for Fedora 20 Unversioned Docdirs no files are included accidentally
- include the sample config files again (instead of just an empty docdir
  that has been added for #846735)
- don't include librbd.so.1 also in -devel package (#1003202)
- move one misplaced rados plugin from -devel into -libs package (#891993)
- include missing directories in -devel and -libs packages
- move librados-config into the -devel pkg where its manual page is, too
- add %%_isa to subpackage dependencies
- don't use %%defattr anymore
- add V=1 to make invocation for verbose build output

* Wed Jul 31 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.61.7-2
- re-enable tmalloc on arm now gperftools is fixed

* Mon Jul 29 2013 Josef Bacik <josef@toxicpanda.com> - 0.61.7-1
- Update to 0.61.7

* Sat Jul 27 2013 pmachata@redhat.com - 0.56.4-2
- Rebuild for boost 1.54.0

* Fri Mar 29 2013 Josef Bacik <josef@toxicpanda.com> - 0.56.4-1
- Update to 0.56.4
- Add upstream d02340d90c9d30d44c962bea7171db3fe3bfba8e to fix logrotate

* Wed Feb 20 2013 Josef Bacik <josef@toxicpanda.com> - 0.56.3-1
- Update to 0.56.3

* Mon Feb 11 2013 Richard W.M. Jones <rjones@redhat.com> - 0.53-2
- Rebuilt to try to fix boost dependency problem in Rawhide.

* Thu Nov  1 2012 Josef Bacik <josef@toxicpanda.com> - 0.53-1
- Update to 0.53

* Mon Sep 24 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.51-3
- Fix automake 1.12 error
- Rebuild after buildroot was messed up

* Tue Sep 18 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.51-2
- Use system leveldb

* Fri Sep 07 2012 David Nalley <david@gnsa.us> - 0.51-1
- Updating to 0.51
- Updated url and source url. 

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Josef Bacik <josef@toxicpanda.com> - 0.46-1
- updated to upstream 0.46
- broke out libcephfs (rhbz# 812975)

* Mon Apr 23 2012 Dan Horák <dan[at]danny.cz> - 0.45-2
- fix detection of C++11 atomic header

* Thu Apr 12 2012 Josef Bacik <josef@toxicpanda.com> - 0.45-1
- updating to upstream 0.45

* Wed Apr  4 2012 Niels de Vos <devos@fedoraproject.org> - 0.44-5
- Add LDFLAGS=-lpthread on any ARM architecture
- Add CFLAGS=-DAO_USE_PTHREAD_DEFS on ARMv5tel

* Mon Mar 26 2012 Dan Horák <dan[at]danny.cz> 0.44-4
- gperftools not available also on ppc

* Mon Mar 26 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.44-3
- Remove unneeded patch

* Sun Mar 25 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.44-2
- Update to 0.44
- Fix build problems

* Mon Mar  5 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.43-1
- Update to 0.43
- Remove upstreamed compile fixes patch
- Remove obsoleted dump_pop patch

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-2
- Rebuilt for c++ ABI breakage

* Thu Feb 16 2012 Tom Callaway <spot@fedoraproject.org> 0.41-1
- update to 0.41
- fix issues preventing build
- rebuild against gperftools

* Sat Dec 03 2011 David Nalley <david@gnsa.us> 0.38-1
- updating to upstream 0.39

* Sat Nov 05 2011 David Nalley <david@gnsa.us> 0.37-1
- create /etc/ceph - bug 745462
- upgrading to 0.37, fixing 745460, 691033
- fixing various logrotate bugs 748930, 747101

* Fri Aug 19 2011 Dan Horák <dan[at]danny.cz> 0.31-4
- google-perftools not available also on s390(x)

* Mon Jul 25 2011 Karsten Hopp <karsten@redhat.com> 0.31-3
- build without tcmalloc on ppc64, BR google-perftools is not available there

* Tue Jul 12 2011 Josef Bacik <josef@toxicpanda.com> 0.31-2
- Remove curl/types.h include since we don't use it anymore

* Tue Jul 12 2011 Josef Bacik <josef@toxicpanda.com> 0.31-1
- Update to 0.31

* Tue Apr  5 2011 Josef Bacik <josef@toxicpanda.com> 0.26-2
- Add the compile fix patch

* Tue Apr  5 2011 Josef Bacik <josef@toxicpanda.com> 0.26
- Update to 0.26

* Tue Mar 22 2011 Josef Bacik <josef@toxicpanda.com> 0.25.1-1
- Update to 0.25.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Steven Pritchard <steve@kspei.com> 0.21.3-1
- Update to 0.21.3.

* Mon Aug 30 2010 Steven Pritchard <steve@kspei.com> 0.21.2-1
- Update to 0.21.2.

* Thu Aug 26 2010 Steven Pritchard <steve@kspei.com> 0.21.1-1
- Update to 0.21.1.
- Sample configs moved to /usr/share/doc/ceph/.
- Added cclass, rbd, and cclsinfo.
- Dropped mkmonfs and rbdtool.
- mkcephfs moved to /sbin.
- Add libcls_rbd.so.

* Tue Jul  6 2010 Josef Bacik <josef@toxicpanda.com> 0.20.2-1
- update to 0.20.2

* Wed May  5 2010 Josef Bacik <josef@toxicpanda.com> 0.20-1
- update to 0.20
- disable hadoop building
- remove all the test binaries properly

* Fri Apr 30 2010 Sage Weil <sage@newdream.net> 0.19.1-5
- Remove java deps (no need to build hadoop by default)
- Include all required librados helpers
- Include fetch_config sample
- Include rbdtool
- Remove misc debugging, test binaries

* Fri Apr 30 2010 Josef Bacik <josef@toxicpanda.com> 0.19.1-4
- Add java-devel and java tricks to get hadoop to build

* Mon Apr 26 2010 Josef Bacik <josef@toxicpanda.com> 0.19.1-3
- Move the rados and cauthtool man pages into the base package

* Sun Apr 25 2010 Jonathan Dieter <jdieter@lesbg.com> 0.19.1-2
- Add missing libhadoopcephfs.so* to file list
- Add COPYING to all subpackages
- Fix ownership of /usr/lib[64]/ceph
- Enhance description of fuse client

* Tue Apr 20 2010 Josef Bacik <josef@toxicpanda.com> 0.19.1-1
- Update to 0.19.1

* Mon Feb  8 2010 Josef Bacik <josef@toxicpanda.com> 0.18-1
- Initial spec file creation, based on the template provided in the ceph src
