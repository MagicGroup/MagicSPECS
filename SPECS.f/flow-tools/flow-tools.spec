%bcond_without  fedora

%global username flow-tools
%global homedir %{_localstatedir}/%{name}
%global gecos "Network flow monitoring"

Version: 0.68.5.1
Name: flow-tools
Summary: Tool set for working with NetFlow data
Summary(zh_CN.UTF-8): 处理 NetFlow 数据的工具集
Release: 17%{?dist}
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License: BSD 
URL: http://code.google.com/p/%{name}/
Source0: http://%{name}.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1: flow-capture.service
Source2: flow-capture.sysconfig
Patch0:  flow-werror-fix.patch
BuildRequires: openssl-devel mysql-devel postgresql-devel zlib-devel 
BuildRequires: bison flex tcp_wrappers-devel
BuildRequires: doxygen
Requires(pre): shadow-utils
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Provides: group(%username)
Provides: user(%username)


%description
Flow-tools is library and a collection of programs used to collect, 
send, process, and generate reports from NetFlow data. The tools can be 
used together on a single server or distributed to multiple servers for 
large deployments. The flow-toools library provides an API for development 
of custom applications for NetFlow export versions 1,5,6 and the 14 currently 
defined version 8 subversions. A Perl and Python interface have been 
contributed and are included in the distribution.

%description -l zh_CN.UTF-8
处理 NetFlow 数据的工具集。

%package devel
Summary: Development files for flow-tools
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release} zlib-devel

%description devel
Flow-tools is library and a collection of programs used to collect,
send, process, and generate reports from NetFlow data. The tools can be
used together on a single server or distributed to multiple servers for
large deployments. The flow-toools library provides an API for development
of custom applications for NetFlow export versions 1,5,6 and the 14 currently
defined version 8 subversions. A Perl and Python interface have been
contributed and are included in the distribution.

This package contains header files required to build applications that use
libft.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package rrdtool
Summary: Scripts for flow-tools to build rrd graphs
Summary(zh_CN.UTF-8): flow-tools 用来建立 rrd 图像的脚本
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: %{name} = %{version}-%{release} rrdtool-python

%description rrdtool
Flow-tools is library and a collection of programs used to collect,
send, process, and generate reports from NetFlow data. The tools can be
used together on a single server or distributed to multiple servers for
large deployments. The flow-toools library provides an API for development
of custom applications for NetFlow export versions 1,5,6 and the 14 currently
defined version 8 subversions. A Perl and Python interface have been
contributed and are included in the distribution.

This package contains scripts that use python-rrdtool to create rrds and graphs
from flow data.

%description rrdtool -l zh_CN.UTF-8
flow-tools 用来建立 rrd 图像的脚本。

%package docs
Summary: HTML and other redundant docs for flow-tools
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: %{name} = %{version}-%{release}

%description docs
Flow-tools is library and a collection of programs used to collect,
send, process, and generate reports from NetFlow data. The tools can be
used together on a single server or distributed to multiple servers for
large deployments. The flow-toools library provides an API for development
of custom applications for NetFlow export versions 1,5,6 and the 14 currently
defined version 8 subversions. A Perl and Python interface have been
contributed and are included in the distribution.

This package contains additional documentation, such as man pages in html format.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
%patch0 -p1

%build
%configure \
  LDFLAGS=-L%{_libdir}/mysql \
  --localstatedir=%{_localstatedir}/%{name} \
  --sysconfdir=%{_sysconfdir}/%{name} \
  --enable-static=no \
  --with-mysql \
  --with-postgresql \
  --with-openssl

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/%{name}
install -d $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %SOURCE1 $RPM_BUILD_ROOT%{_unitdir}/flow-capture.service
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0644 %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/flow-capture

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
    useradd -r -g %{username} -d %{homedir} -s /sbin/nologin \
    -c '%{gecos}' %{username}
exit 0


%post
/sbin/ldconfig
%systemd_post flow-capture.service

%preun
%systemd_preun flow-capture.service

%postun
%systemd_postun

%files 
%doc README README.fork COPYING ChangeLog
%{_mandir}/man1/flow-capture.1*
%{_mandir}/man1/flow-cat.1*
%{_mandir}/man1/flow-dscan.1*
%{_mandir}/man1/flow-expire.1*
%{_mandir}/man1/flow-export.1*
%{_mandir}/man1/flow-fanout.1*
%{_mandir}/man1/flow-filter.1*
%{_mandir}/man1/flow-gen.1*
%{_mandir}/man1/flow-header.1*
%{_mandir}/man1/flow-import.1*
%{_mandir}/man1/flow-mask.1*
%{_mandir}/man1/flow-merge.1*
%{_mandir}/man1/flow-nfilter.1*
%{_mandir}/man1/flow-print.1*
%{_mandir}/man1/flow-receive.1*
%{_mandir}/man1/flow-report.1*
%{_mandir}/man1/flow-rptfmt.1*
%{_mandir}/man1/flow-send.1*
%{_mandir}/man1/flow-split.1*
%{_mandir}/man1/flow-stat.1*
%{_mandir}/man1/flow-tag.1*
%{_mandir}/man1/flow-tools-examples.1*
%{_mandir}/man1/flow-tools.1*
%{_mandir}/man1/flow-xlate.1*
%{_bindir}/flow-capture
%{_bindir}/flow-cat
%{_bindir}/flow-dscan
%{_bindir}/flow-expire
%{_bindir}/flow-export
%{_bindir}/flow-fanout
%{_bindir}/flow-filter
%{_bindir}/flow-gen
%{_bindir}/flow-header
%{_bindir}/flow-import
%{_bindir}/flow-mask
%{_bindir}/flow-merge
%{_bindir}/flow-nfilter
%{_bindir}/flow-print
%{_bindir}/flow-receive
%{_bindir}/flow-report
%{_bindir}/flow-rptfmt
%{_bindir}/flow-send
%{_bindir}/flow-split
%{_bindir}/flow-stat
%{_bindir}/flow-tag
%{_bindir}/flow-xlate
%{_libdir}/*.so.*
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/cfg/
%dir %{_sysconfdir}/%{name}/sym/
%config(noreplace) %{_sysconfdir}/%{name}/cfg/*
%config(noreplace) %{_sysconfdir}/%{name}/sym/*
%config(noreplace) %{_sysconfdir}/sysconfig/flow-capture
%{_unitdir}/flow-capture.service
%attr(-,flow-tools,flow-tools) %{_localstatedir}/%{name}/
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*

%files devel
%{_libdir}/*.so
%{_includedir}/*.h

%files rrdtool
%{_bindir}/flow-rpt2rrd
%{_bindir}/flow-log2rrd
%{_mandir}/man1/flow-rpt2rrd.1*
%{_mandir}/man1/flow-log2rrd.1*

%files docs
%doc docs/*.html ChangeLog.old TODO INSTALL SECURITY

%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.68.5.1-17
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.68.5.1-14
- fix syslog() calls to have string format

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Paul Komkoff <i@stingr.net> - 0.68.5.1-12
- bz#850114

* Sat Sep 28 2013 Paul Komkoff <i@stingr.net> - 0.68.5.1-11
- Try to fix bz#1013218 as per https://fedoraproject.org/wiki/Packaging:UsersAndGroups

* Fri Aug 23 2013 i@stingr.net - 0.68.5.1-10
- Try to fix bz#929362

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Jon Ciesla <limburgher@gmail.com> - 0.68.5.1-8
- Migrate from fedora-usermgmt to guideline scriptlets.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Jon Ciesla <limburgher@gmail.com> - 0.68.5.1-5
- Migrate to systemd, BZ 767392.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 28 2011 Orion Poplawski <orion@cora.nwra.com> - 0.68.5.1-3
- Rebuild for new mysql
- Add LDFLAGS for mysql on 64-bit

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 27 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.68.5.1
- fix for EINTR while reading/writing in ftio.

* Thu Feb 25 2010 Paul P Komkoff Jr <i@stingr.net> - 0.68.5
- bunch of fixes from upstream

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.68.4.1-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Paul P Komkoff Jr <i@stingr.net> - 0.68.4.1-1
- fix for pcap generation, by Dave Plonka
- split out -rrdtool subpackage, for those who don't need rrdtool on their servers.

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> - 0.68.4-2
- rebuild for dependencies

* Mon Mar 31 2008 Paul P Komkoff Jr <i@stingr.net> - 0.68.4-1
- New upstream version

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.68.4-0.2.rc1
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Paul P Komkoff Jr <i@stingr.net> - 0.68.4-0.1.rc1
- new upstream release candidate

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.68.3-2
- Rebuild for deps

* Mon Nov 12 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68.3-1
- new upstream release
- build tools as PIE
- get rid of ftpaths.h
- do not ship ftconfig.c
- do not require libft

* Sat Nov  3 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68.2-1
- New upstream release

* Thu Sep 13 2007 Orion Poplawski <orion@cora.nwra.com> - 0.68.1-2
- Add user and init scripts

* Sun Aug  5 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68.1-1
- New upstream release

* Sun Jul 15 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68.1-0.1.rc3
- New upstream rc

* Sun Jul 15 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68.1-0.1.rc2
- Switch to 0.68.1 fork
- Drop all patches
- Sanitize spec

* Sun Mar 25 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68-16
- getopt() is now in unistd.h

* Sun Mar 18 2007 Paul P Komkoff Jr <i@stingr.net> - 0.68-15
- Add runtime dependency for python-rrdtool

* Fri Dec 15 2006 Paul P. Komkoff Jr <i@stingr.net>
- rebuilt

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.68-13
- Rebuild for new Postgres

* Thu Nov 16 2006 Paul P Komkoff Jr <i@stingr.net> - 0.68-12
- Fix flow report 72 (by reaper@surnet.ru) bz#212928

* Sun Sep 10 2006 Paul P Komkoff Jr <i@stingr.net> - 0.68-11
- rebuild

* Sun Jul  9 2006 Paul P Komkoff Jr <i@stingr.net> 0.68-10
- Rebuild

* Sun Jul  9 2006 Paul P Komkoff Jr <i@stingr.net> 0.68-9
- Fix build in mock with minimal build environment #197706

* Sat Jun 10 2006 Paul P Komkoff Jr <i@stingr.net> 0.68-8
- Split patches in more convenient way (and bug upstream)
- Fix 2 unitialized variable bugs

* Sun Feb 19 2006 Paul P Komkoff Jr <i@stingr.net> 0.68-7
- Rebuild

* Mon Nov 14 2005 Paul P Komkoff Jr <i@stingr.net> 0.68-6
- Rebuild

* Sun Oct 30 2005 Paul P Komkoff Jr <i@stingr.net> 0.68-5
- Fix flow-capture segfaults on platforms with 64bit time_t

* Thu Oct 20 2005 Paul P Komkoff Jr <i@stingr.net> 0.68-4
- Fix accidential damage

* Wed Oct 19 2005 Paul P Komkoff Jr <i@stingr.net> 0.68-3
- add zlib-devel to build-requires of main package and to
  requires of -devel package

* Tue Sep  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.68-2
- simplify %%files
- use more macros
- change Group to Application/System
- own/create %{_localstatedir}/ft/
- add BR: autoconf
- don't need generic INSTALL
- mark config files as such
- own all directories we create
- run ldconfig on post/postun

* Tue Sep  6 2005 Paul P Komkoff Jr <i@stingr.net> 0.68-1
- Submit to fedora-extras
- Change volatile data location to /var/ft and nonvolatile
  to /etc/flow-tools (FHS)
- Make libft shared library
- Split to plain/devel

* Fri Jan  7 2004 William Emmanuel S. Yu <wyu@ateneo.edu>
- updated RPM file for version 0.67

* Tue Aug  8 2003 William Emmanuel S. Yu <wyu@ateneo.edu>
- fixed SQL bug
- update flow-export documentation

* Tue Apr 29 2003 William Emmanuel S. Yu <wyu@ateneo.edu>
- add support for checking null symbols filename

* Fri Apr  4 2003 William Emmanuel S. Yu <wyu@ateneo.edu>
- updated RPM file for version 0.66

* Fri Apr  4 2003 William Emmanuel S. Yu <wyu@ateneo.edu>
- updated RPM file for version 0.65
- included PostgreSQL support patch

* Mon Feb  3 2003 Larry Fahnoe <fahnoe@FahnoeTech.com>
- added makefile patches to use RPM_OPT_FLAGS
- added manpages and html files to spec file

* Tue Dec 17 2002 William Emmanuel S. Yu <wyu@ateneo.edu>
- added tagging and ip-port patches

* Thu Dec 12 2002 William Emmanuel S. Yu <wyu@ateneo.edu>
- updated RPM file for version 0.63

* Wed Oct 16 2002 William Emmanuel S. Yu <wyu@ateneo.edu>
- initial creation of RPM file for version 0.62
