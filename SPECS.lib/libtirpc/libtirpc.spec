%define _root_libdir    %{_libdir}

Name:		   libtirpc
Version: 0.2.4
Release: 1%{?dist}
Summary:		Transport Independent RPC Library
Summary(zh_CN.UTF-8): 独立运行的 RPC 库
Group:		  	System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:		SISSL and BSD
URL:  			http://nfsv4.bullopensource.org/

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	http://downloads.sourceforge.net/libtirpc/libtirpc-%{version}.tar.bz2

Patch001: libtirpc-0.2.5-rc3.patch

BuildRequires:		automake, autoconf, libtool, pkgconfig
BuildRequires:		libgssglue-devel

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of 
Open Network Computing (ONC), and is derived directly from the 
Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V 
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface 
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported 
by almost 70 vendors on all major operating systems.  TS-RPC source code 
(RPCSRC 4.0) remains available from several internet sites.

%description -l zh_CN.UTF-8
独立运行的 RPC 库。

%package devel
Summary:	Development files for the libtirpc library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:	Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig man-db

%description devel
This package includes header files and libraries necessary for
developing programs which use the tirpc library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%patch001 -p1

# Remove .orig files
find . -name "*.orig" | xargs rm -f

%build
sh autogen.sh
autoreconf -fisv
%configure --enable-gss
make all

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}%{_root_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
make install DESTDIR=%{buildroot} \
	libdir=%{_root_libdir} pkgconfigdir=%{_libdir}/pkgconfig
# Don't package .a or .la files
rm -f %{buildroot}%{_root_libdir}/*.{a,la}

# Creat the man diretory
mv %{buildroot}%{_mandir}/man3 %{buildroot}%{_mandir}/man3t

magic_rpm_clean.sh

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
# Register the new man section
#if [ "$1" -eq 1 ]; then
#	makewhatis -s 3t	
#fi

%postun devel 
# Remove the existance of the man section
#makewhatis -s 3t


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_root_libdir}/libtirpc.so.*
%config(noreplace)%{_sysconfdir}/netconfig

%files devel
%defattr(0644,root,root,755)
%dir %{_includedir}/tirpc
%dir %{_includedir}/tirpc/rpc
%dir %{_includedir}/tirpc/rpcsvc
%{_root_libdir}/libtirpc.so
%{_libdir}/pkgconfig/libtirpc.pc
%{_includedir}/tirpc/netconfig.h
%{_includedir}/tirpc/rpc/auth.h
%{_includedir}/tirpc/rpc/auth_des.h
%{_includedir}/tirpc/rpc/auth_gss.h
%{_includedir}/tirpc/rpc/auth_kerb.h
%{_includedir}/tirpc/rpc/auth_unix.h
%{_includedir}/tirpc/rpc/clnt.h
%{_includedir}/tirpc/rpc/clnt_soc.h
%{_includedir}/tirpc/rpc/clnt_stat.h
%{_includedir}/tirpc/rpc/des.h
%{_includedir}/tirpc/rpc/des_crypt.h
%{_includedir}/tirpc/rpc/nettype.h
%{_includedir}/tirpc/rpc/pmap_clnt.h
%{_includedir}/tirpc/rpc/pmap_prot.h
%{_includedir}/tirpc/rpc/pmap_rmt.h
%{_includedir}/tirpc/rpc/raw.h
%{_includedir}/tirpc/rpc/rpc.h
%{_includedir}/tirpc/rpc/rpc_com.h
%{_includedir}/tirpc/rpc/rpc_msg.h
%{_includedir}/tirpc/rpc/rpcb_clnt.h
%{_includedir}/tirpc/rpc/rpcb_prot.h
%{_includedir}/tirpc/rpc/rpcb_prot.x
%{_includedir}/tirpc/rpc/rpcent.h
%{_includedir}/tirpc/rpc/svc.h
%{_includedir}/tirpc/rpc/svc_auth.h
%{_includedir}/tirpc/rpc/svc_dg.h
%{_includedir}/tirpc/rpc/svc_soc.h
%{_includedir}/tirpc/rpc/types.h
%{_includedir}/tirpc/rpc/xdr.h
%{_includedir}/tirpc/rpcsvc/crypt.h
%{_includedir}/tirpc/rpcsvc/crypt.x
%{_mandir}/*/*

%changelog
* Fri Aug 01 2014 Liu Di <liudidi@gmail.com> - 0.2.4-1
- 更新到 0.2.4

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.2.2-4
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 0.2.2-3
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.2.2-2
- 为 Magic 3.0 重建

* Tue Jun 21 2011 Steve Dickson  <steved@redhat.com> 0.2.1-1
- Updated to latest upstream version: 0.2.3-rc1

* Mon May  2 2011 Steve Dickson  <steved@redhat.com> 0.2.1-0
- Updated to latest upstream version: 0.2.2

* Tue Apr 12 2011 Karsten Hopp <karsten@redhat.com> 0.2.1-7.1
- replace Requires(devel) with a simple Requires as the new rpm
  aborts otherwise with "Bad Requireflags: qualifiers: Requires(devel)"

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Steve Dickson  <steved@redhat.com> 0.2.1-6
- Moved the libraries from /usr/lib to /lib 

* Mon Aug 30 2010 Steve Dickson  <steved@redhat.com> 0.2.1-5
- Relicense these SISSL files to 3 clause BSD
- Fixed last remaining BSD license issues

* Fri Jul 16 2010 Steve Dickson  <steved@redhat.com> 0.2.1-4
- Add back SISSL license attribution

* Fri Jul 09 2010 Mike McGrath <mmcgrath@redhat.com> 0.2.1-3.1
- Rebuild to fix broken man dep s/man/man-db/

* Tue May 18 2010 Steve Dickson  <steved@redhat.com> 0.2.1-3
- Updated to latest RC release: libtirpc-0-2-2-rc2 [bz 519430]

* Mon Mar 22 2010 Steve Dickson  <steved@redhat.com> 0.2.1-2
- Updated to latest RC release: libtirpc-0-2-2-rc1

* Mon Nov 30 2009 Steve Dickson  <steved@redhat.com> 0.2.1-1
- Updated to latest upstream version: 0.2.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Steve Dickson  <steved@redhat.com> 0.2.0-3
- Updated to latest upstream tag: 0-2-1-rc3
    Fixed the --disable-gss options
    Fixed a number of warnings
    Change how architectures are define in xdr_float.c

* Mon Jun 29 2009 Steve Dickson  <steved@redhat.com> 0.2.0-2
- Updated to latest upstream tag: 0-2-1-rc2
    rpcb_clnt: RPC_PROGNOTREGISTERED is a permanent error
    clnt_dg: Fix infinite loop when datagram call times ou
    Updated .gitignore file
    Replace the hard coded path name with the top_srcdir macrc
    Added 'doc' to the SUBDIRS list so make install work correctly.

* Fri May 29 2009 Steve Dickson  <steved@redhat.com> 0.2.0-1
- Updated to latest upstream version: 0.2.0

* Tue May 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.11-3
- Replace the Sun RPC license with the BSD license, with the explicit permission of Sun Microsystems

* Mon Apr 20 2009 Steve Dickson  <steved@redhat.com> 0.1.11-2
- Updated to libtirpc-0.1.12-rc1

* Mon Apr 20 2009 Steve Dickson  <steved@redhat.com> 0.1.11-1
- Updated to the latest release: 0.1.11 

* Fri Mar 13 2009 Steve Dickson  <steved@redhat.com> 0.1.10-6
- libtirpc: set r_netid and r_owner in __rpcb_findaddr_timed
- libtirpc: be sure to free cl_netid and cl_tp
- libtirpc: must free saved wire verifier when destroying context

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Steve Dickson  <steved@redhat.com> 0.1.10-4
- Converted all uids and uids to type uid_t and gid_t (sf 2446314)

* Wed Jan 28 2009 Steve Dickson  <steved@redhat.com> 0.1.10-3
- backwards compatibility: fix order of fields in TI-RPC's 
  svc_req (bz 481388)
- Removed a number warnings.

* Thu Jan 22 2009 Steve Dickson  <steved@redhat.com> 0.1.10-2
- Header file fixes for C++

* Thu Nov 20 2008 Steve Dickson  <steved@redhat.com> 0.1.10-1
- Updated to latest upstream version: 0.1.10

* Tue Oct 28 2008 Steve Dickson  <steved@redhat.com> 0.1.9-7
- Fixed some incorrect function declarations (bz468815)

* Mon Oct 27 2008 Steve Dickson  <steved@redhat.com> 0.1.9-6
- Fix bad assumption taddr2uaddr processing that 
  caused a segfault (bz468014)

* Tue Sep 16 2008 Steve Dickson <steved@redhat.com> 0.1.9-5
- Fix for taddr2addr conversion bug of local addresses
- Fixed some of warnings in: src/auth_time.c, src/clnt_dg.c and
  src/clnt_raw.c
- Added some #ifdef NOTUSED around some code in src/rpbc_clnt.c
  that was not being used...

* Thu Sep  4 2008 Steve Dickson <steved@redhat.com> 0.1.9-4
- Always make IPv6 sockets V6ONLY
- Fix incorrect sizeof() in __rpc_getbroadifs

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.9-3
- fix license tag

* Tue Jul 9 2008 Steve Dickson  <steved@redhat.com> 0.1.9-1
- Update to latest upstream version 0.1.9

* Fri Jun 27 2008 Steve Dickson  <steved@redhat.com> 0.1.8-2
- Added super-H(sh3,4) architecture support (bz 446559)

* Tue Jun 10 2008 Steve Dickson  <steved@redhat.com> 0.1.8-1
- Update to latest upstream version 0.1.8

* Wed Mar 12 2008 Steve Dickson  <steved@redhat.com> 0.1.7-18
- Install man pages in the 3t section

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.7-17
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Steve Dickson  <steved@redhat.com> 0.1.7-16
- Added patch that creates a libtirpc.pc used by the
  pkg-config command.

* Thu Jan 24 2008 Steve Dickson  <steved@redhat.com> 0.1.7-15
- Protect from buffer overflow in the GSS code. (bz 362121)

* Mon Dec 17 2007 Steve Dickson  <steved@redhat.com> 0.1.7-14
- Fixed typo in /etc/netconfig file (bz 414471)

* Thu Oct 25 2007 Steve Dickson  <steved@redhat.com> 0.1.7-13
- Added a check for the ARM arch (bz 351071)

* Wed Oct 17 2007 Steve Dickson  <steved@redhat.com> 0.1.7-12
- Switch the libgssapi dependency to libgssglue

* Mon Oct 15 2007 Steve Dickson  <steved@redhat.com> 0.1.7-11
- Made tcp6/udp6 network ids no longer visible in the netconfig
  file since the ipv6 code is not fully baked yet in rpcbind. (bz 249121)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.1.7-10
- Rebuild for selinux ppc32 issue.

* Mon Jul 30 2007 <steved@redhat.com> 0.1.7-9
- Fixed mutex lock problem in clnt_raw_create()
- Ignore the return value of snprintf() and use strlen() instead
  to bump the pointer in clnt_sperror()
- A couple ntohs() were needed in bindresvport_sa()
- Added IP_RECVERR processing with to clnt_dg_call() so
  application will see errors instead of timing out
- Make sure remote address (xp_rtaddr) is populated
  with the correct type of address.
- Change the order of network ids in /etc/netconfg
  putting ipv4 ids before ipv6.
- Bumped up Release from 8 to 9.

* Mon Jul  9 2007 <steved@redhat.com> 0.1.7-7
- Fixed infinite loop in svc_run() (bz 246677)

* Thu Apr 26 2007 <steved@redhat.com> 0.1.7-6
- Fixed potential buffer overflow in xdr_strings
- Added a optimization to bindresvport that allows more
  ports to be tried.

* Mon Mar 26 2007 Steve Dickson <steved@redhat.com> 0.1.7-5
- Fixed Unowned Directory RPM problem (bz 233873)

* Mon Aug 28 2006 Steve Dickson <steved@redhat.com> 0.1.7-4
- Fixed undefined symbol (bz 204296)

* Mon Aug 14 2006 Steve Dickson <steved@redhat.com> 0.1.7-3
- Added in svc_auth_none needed by the GSSAPI code.
- Added compile define for ppc64 archs

* Fri Aug 11 2006 Steve Dickson <steved@redhat.com> 0.1.7-2
- Uncommented tcp6 and udp6 in the default /etc/netconfig file.
- Added hooks to used the libgssapi library.

* Fri Aug  4 2006 Steve Dickson <steved@redhat.com> 0.1.7-1
- Initial commit
