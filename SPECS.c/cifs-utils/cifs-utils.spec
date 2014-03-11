#% define pre_release rc1
%define pre_release %nil

Name:           cifs-utils
Version:	6.3
Release:        1%{pre_release}%{?dist}
Summary:        Utilities for mounting and managing CIFS mounts
Summary(zh_CN.UTF-8): 挂载和管理 CIFS 的工具

Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License:        GPLv3
URL:            http://linux-cifs.samba.org/cifs-utils/
BuildRoot:      %{_tmppath}/%{name}-%{version}%{pre_release}-%{release}-root-%(%{__id_u} -n)

Source0:        ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}%{pre_release}.tar.bz2

BuildRequires:  libcap-ng-devel libtalloc-devel krb5-devel keyutils-libs-devel autoconf automake libwbclient-devel
Requires:       keyutils

%description
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains tools for mounting
shares on Linux using the SMB/CIFS protocol. The tools in this package
work in conjunction with support in the kernel to allow one to mount a
SMB/CIFS share onto a client and use it as if it were a standard Linux
file system.

%description -l zh_CN.UTF-8
SMB/CIFS 协议是微软 Windows 使用的标准文件分享协议，这个包包含了在 Linux 
上挂载这些共享文件的工具。

%prep
%setup -q -n %{name}-%{version}%{pre_release}

%build
%configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
/sbin/mount.cifs
%{_bindir}/getcifsacl
%{_bindir}/setcifsacl
%{_bindir}/cifscreds
%{_sbindir}/cifs.upcall
%{_sbindir}/cifs.idmap
%{_includedir}/cifsidmap.h
%{_libdir}/cifs-utils/idmapwb.so
%{_libdir}/security/pam_cifscreds.so
%{_mandir}/man8/idmapwb.8.gz
%{_mandir}/man8/pam_cifscreds.8.gz
%{_mandir}/man1/getcifsacl.1.gz
%{_mandir}/man1/setcifsacl.1.gz
%{_mandir}/man1/cifscreds.1.gz
%{_mandir}/man8/cifs.upcall.8.gz
%{_mandir}/man8/cifs.idmap.8.gz
%{_mandir}/man8/mount.cifs.8.gz
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf

%changelog
* Tue Mar 11 2014 Liu Di <liudidi@gmail.com> - 6.3-1
- 更新到 6.3

* Sun Nov 11 2012 Jeff Layton <jlayton@redhat.com> 5.8-1
- update to 5.8

* Wed Nov 07 2012 Jeff Layton <jlayton@redhat.com> 5.7-3
- update to latest patches queued for 5.8. More idmapping and ACL tool fixes.

* Sun Nov 04 2012 Jeff Layton <jlayton@redhat.com> 5.7-2
- update to latest patches queued for 5.8. Mostly idmapping and ACL tool fixes.

* Tue Oct 09 2012 Jeff Layton <jlayton@redhat.com> 5.7-1
- update to 5.7

* Fri Aug 24 2012 Jeff Layton <jlayton@redhat.com> 5.6-2
- update to current upstream head

* Thu Jul 26 2012 Jeff Layton <jlayton@redhat.com> 5.6-1
- update to 5.6

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Jeff Layton <jlayton@redhat.com> 5.5-2
- remove -Werror flag
- enable PIE and RELRO

* Wed May 30 2012 Jeff Layton <jlayton@redhat.com> 5.5-1
- update to 5.5

* Wed Apr 25 2012 Jeff Layton <jlayton@redhat.com> 5.4-2
- rebuild to fix dependencies due to libwbclient changes

* Wed Apr 18 2012 Jeff Layton <jlayton@redhat.com> 5.4-1
- update to 5.4
- add patch to fix up more warnings

* Mon Mar 19 2012 Jeff Layton <jlayton@redhat.com> 5.3-4
- fix tests for strtoul success (bz# 800621)

* Wed Feb 08 2012 Jeff Layton <jlayton@redhat.com> 5.3-3
- revert mount.cifs move. It's unnecessary at this point.

* Wed Feb 08 2012 Jeff Layton <jlayton@redhat.com> 5.3-2
- move mount.cifs to /usr/sbin per new packaging guidelines

* Sat Jan 28 2012 Jeff Layton <jlayton@redhat.com> 5.3-1
- update to 5.3

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Jeff Layton <jlayton@redhat.com> 5.2-2
- add /etc/request-key.d files

* Fri Dec 09 2011 Jeff Layton <jlayton@redhat.com> 5.2-1
- update to 5.2

* Fri Sep 23 2011 Jeff Layton <jlayton@redhat.com> 5.1-1
- update to 5.1
- add getcifsacl and setcifsacl to package

* Fri Jul 29 2011 Jeff Layton <jlayton@redhat.com> 5.0-2
- mount.cifs: fix check_newline retcode check (bz# 726717)

* Wed Jun 01 2011 Jeff Layton <jlayton@redhat.com> 5.0-1
- update to 5.0

* Mon May 16 2011 Jeff Layton <jlayton@redhat.com> 4.9-2
- mount.cifs: pass unadulterated device string to kernel (bz# 702664)

* Fri Mar 04 2011 Jeff Layton <jlayton@redhat.com> 4.9-1
- update to 4.9

* Tue Feb 08 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-4
- mount.cifs: reenable CAP_DAC_READ_SEARCH when mounting (bz# 675761)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-2
- mount.cifs: don't update mtab if it's a symlink (bz# 674101)

* Fri Jan 21 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-1
- update to 4.8.1

* Sat Jan 15 2011 Jeff Layton <jlayton@redhat.com> 4.8-1
- update to 4.8

* Tue Oct 19 2010 Jeff Layton <jlayton@redhat.com> 4.7-1
- update to 4.7

* Fri Jul 30 2010 Jeff Layton <jlayton@redhat.com> 4.6-1
- update to 4.6

* Tue Jun 01 2010 Jeff Layton <jlayton@redhat.com> 4.5-2
- mount.cifs: fix parsing of cred= option (BZ#597756)

* Tue May 25 2010 Jeff Layton <jlayton@redhat.com> 4.5-1
- update to 4.5

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-3
- mount.cifs: fix regression in prefixpath patch

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-2
- mount.cifs: strip leading delimiter from prefixpath

* Wed Apr 28 2010 Jeff Layton <jlayton@redhat.com> 4.4-1
- update to 4.4

* Sat Apr 17 2010 Jeff Layton <jlayton@redhat.com> 4.3-2
- fix segfault when address list is exhausted (BZ#583230)

* Fri Apr 09 2010 Jeff Layton <jlayton@redhat.com> 4.3-1
- update to 4.3

* Fri Apr 02 2010 Jeff Layton <jlayton@redhat.com> 4.2-1
- update to 4.2

* Tue Mar 23 2010 Jeff Layton <jlayton@redhat.com> 4.1-1
- update to 4.1

* Mon Mar 08 2010 Jeff Layton <jlayton@redhat.com> 4.0-2
- fix bad pointer dereference in IPv6 scopeid handling

* Wed Mar 03 2010 Jeff Layton <jlayton@redhat.com> 4.0-1
- update to 4.0
- minor specfile fixes

* Fri Feb 26 2010 Jeff Layton <jlayton@redhat.com> 4.0-1rc1
- update to 4.0rc1
- fix prerelease version handling

* Mon Feb 08 2010 Jeff Layton <jlayton@redhat.com> 4.0a1-1
- first RPM package build

