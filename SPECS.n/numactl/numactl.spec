Name:		numactl
Summary:	Library for tuning for Non Uniform Memory Access machines
Summary(zh_CN.UTF-8): 调整非一致内存访问机的库
Version: 2.0.10
Release: 2%{?dist}
License:	LGPLv2/GPLv2
Group:		System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL:		ftp://oss.sgi.com/www/projects/libnuma/download
Source0:	ftp://oss.sgi.com/www/projects/libnuma/download/numactl-%{version}.tar.gz
Buildroot:	%{_tmppath}/%{name}-buildroot

ExcludeArch: s390 s390x %{arm}

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy.

%description -l zh_CN.UTF-8
调整非一致内存访问机的库。

%package libs
Summary: libnuma libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
numactl-libs provides libnuma, a library to do allocations with
NUMA policy in applications.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary: Development package for building Applications that use numa
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}-libs = %{version}-%{release}

%description devel
Provides development headers for numa library calls

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{version}

%build
./autogen.sh
./configure --prefix=/usr --libdir=%{_libdir}
make clean
make CFLAGS="$RPM_OPT_FLAGS -I."

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%post libs -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/numactl
%{_bindir}/numademo
%{_bindir}/numastat
%{_bindir}/memhog
%{_bindir}/migspeed
%{_bindir}/migratepages
%{_mandir}/man8/*.8*
%exclude %{_mandir}/man2/*.2*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libnuma.so.1.0.0
%{_libdir}/libnuma.so.1

%files devel
%defattr(-,root,root,-)
%{_libdir}/libnuma.so
%exclude %{_libdir}/libnuma.a
%exclude %{_libdir}/libnuma.la
%{_includedir}/numa.h
%{_includedir}/numaif.h
%{_includedir}/numacompat1.h
%{_mandir}/man3/*.3*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.0.10-2
- 为 Magic 3.0 重建

* Sat Feb 28 2015 Liu Di <liudidi@gmail.com> - 2.0.10-1
- 更新到 2.0.10

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.0.7-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Petr Holasek <pholasek@redhat.com> - 2.0.7-6
- numademo segfault fix (bz823125, bz823127)

* Sun Apr 15 2012 Petr Holasek <pholasek@redhat.com> - 2.0.7-5
- Library splitted out of numactl package to numactl-libs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 01 2012 Anton Arapov <anton@redhat.com> - 2.0.7-3
- Include missing manpages

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> - 2.0.7-2
- Exclude ARM platforms

* Fri Apr 15 2011 Anton Arapov <anton@redhat.com> - 2.0.7-1
- Update to latest upstream stable version (bz 696703)

* Tue Mar 22 2011 Anton Arapov <anton@redhat.com> - 2.0.6-2
- Better manpages (bz 673613)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Neil Horman <nhorman@redhat.com> - 2.0.6-1
- Update to latest upstream stable version (bz 666379)

* Mon Oct 18 2010 Neil Horman <nhorman@redhat.com> - 2.0.5-1
- Update to latest stable upstream source

* Mon Feb 15 2010 Neil Horman <nhorman@redhat.com> - 2.0.3-8
- Remove static libs from numactl (bz 556088)

* Mon Aug 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.3-7
- Add destructor to libnuma.so to free allocated memory (bz 516227)

* Mon Aug 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.3-6
- Fix obo in nodes_allowed_list strncpy (bz 516223)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Neil Horman <nhorman@redhat.com>
- Update to full 2.0.3 version (bz 506795)

* Wed Jun 17 2009 Neil Horman <nhorman@redhat.com>
- Fix silly libnuma warnings again (bz 499633)

* Fri May 08 2009 Neil Horman <nhorman@redhat.com>
- Update to 2.0.3-rc3 (bz 499633)

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2.0.2-4
- Remove warning from libnuma (bz 484552)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.2-2
- Fix build break due to register selection in asm

* Mon Sep 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.2-1
- Update rawhide to version 2.0.2 of numactl

* Fri Apr 25 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-6
- Fix buffer size passing and arg sanity check for physcpubind (bz 442521)

* Fri Mar 14 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-5
- Fixing spec file to actually apply alpha patch :)

* Fri Mar 14 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-4
- Add alpha syscalls (bz 396361)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-3
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update numactl to fix get_mempolicy signature (bz 418551)

* Fri Dec 14 2007 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update numactl to latest version (bz 425281)

* Tue Aug 07 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-4
- Fixing some remaining merge review issues (bz 226207)

* Fri Aug 03 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-3
- fixing up merge review (bz 226207)

* Fri Jan 12 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-2
- Properly fixed bz 221982
- Updated revision string to include %{dist}

* Thu Jan 11 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-1.38
- Fixed -devel to depend on base package so libnuma.so resolves

* Thu Sep 21 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.36
- adding nodebind patch for bz 207404

* Fri Aug 25 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.35
- moving over libnuma.so to -devel package as well

* Fri Aug 25 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.34
- split out headers/devel man pages to a devel subpackage

* Tue Aug 15 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.32
- add patch for broken cpu/nodebind output (bz 201906)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8-1.31
- rebuild

* Tue Jun 13 2006 Neil Horman <nhorman@redhat.com>
- Rebased numactl to version 0.9.8 for FC6/RHEL5

* Wed Apr 26 2006 Neil Horman <nhorman@redhat.com>
- Added patches for 64 bit overflows and cpu mask problem

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com>
- rebuild for ppc TLS issue (#184446)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.4-1.25.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jul  7 2005 Dave Jones <davej@redhat.com>
- numactl doesn't own the manpage dirs. (#161547)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- rebuild with -D_FORTIFY_SOURCE=2

* Wed Nov 10 2004 David Woodhouse <dwmw2@redhat.com>
- Fix build on x86_64

* Thu Oct 21 2004 David Woodhouse <dwmw2@redhat.com>
- Add PPC support

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun 05 2004 Warren Togami <wtogami@redhat.com> 
- spec cleanup

* Sat Jun 05 2004 Arjan van de Ven <arjanv@redhat.com>
- initial packaging

