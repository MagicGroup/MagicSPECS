Name: libteam
Version: 1.11
Release: 3%{?dist}
Summary: Library for controlling team network device
Group: System Environment/Libraries
License: LGPLv2+
URL: http://www.libteam.org
Source: http://www.libteam.org/files/libteam-%{version}.tar.gz
BuildRequires: jansson-devel
BuildRequires: libdaemon-devel
BuildRequires: libnl3-devel
BuildRequires: python-devel
BuildRequires: dbus-devel
BuildRequires: swig

%description
This package contains a library which is a user-space
counterpart for team network driver. It provides an API
to control team network devices.

%package devel
Group: Development/Libraries
Summary: Libraries and header files for libteam development
Requires: libteam = %{version}-%{release}

%package -n teamd
Group: System Environment/Daemons
Summary: Team network device control daemon
Requires: libteam = %{version}-%{release}

%package -n teamd-devel
Group: Development/Libraries
Summary: Libraries and header files for teamd development
Requires: teamd = %{version}-%{release}

%package -n python-libteam
Group: Development/Libraries
Summary: Team network device library bindings
Requires: libteam = %{version}-%{release}

%description devel
The libteam-devel package contains the header files and libraries
necessary for developing programs using libteam.

%description -n teamd
The teamd package contains team network device control daemon.

%description -n teamd-devel
The teamd-devel package contains the header files and libraries
necessary for developing programs using libteamdctl.

%description -n python-libteam
The team-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by team network device library.

This package should be installed if you want to develop Python
programs that will manipulate team network devices.

%prep
%setup -q

# prepare example dir for -devel
mkdir -p _tmpdoc1/examples
cp -p examples/*.c _tmpdoc1/examples
# prepare example dir for team-python
mkdir -p _tmpdoc2/examples
cp -p examples/python/*.py _tmpdoc2/examples
chmod -x _tmpdoc2/examples/*.py

%build
%configure --disable-static
make %{?_smp_mflags}
cd binding/python
python ./setup.py build

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -delete
rm -rf $RPM_BUILD_ROOT/%{_bindir}/team_*
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
install -p teamd/dbus/teamd.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p teamd/redhat/systemd/teamd@.service $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-Team $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-Team $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-TeamPort $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-TeamPort $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 utils/bond2team $RPM_BUILD_ROOT%{_bindir}/bond2team
cd binding/python
python ./setup.py install --root $RPM_BUILD_ROOT -O1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libteam.so.*
%{_bindir}/teamnl
%{_mandir}/man8/teamnl.8*

%files devel
%doc COPYING _tmpdoc1/examples
%{_includedir}/team.h
%{_libdir}/libteam.so
%{_libdir}/pkgconfig/libteam.pc

%files -n teamd
%doc COPYING teamd/example_configs teamd/redhat/example_ifcfgs/
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/teamd.conf
%config(noreplace) %attr(644,root,root) %{_unitdir}/teamd@.service
%{_sysconfdir}/sysconfig/network-scripts/ifup-Team
%{_sysconfdir}/sysconfig/network-scripts/ifdown-Team
%{_sysconfdir}/sysconfig/network-scripts/ifup-TeamPort
%{_sysconfdir}/sysconfig/network-scripts/ifdown-TeamPort
%{_libdir}/libteamdctl.so.*
%{_bindir}/teamd
%{_bindir}/teamdctl
%{_bindir}/bond2team
%{_mandir}/man8/teamd.8*
%{_mandir}/man8/teamdctl.8*
%{_mandir}/man5/teamd.conf.5*
%{_mandir}/man1/bond2team.1*

%files -n teamd-devel
%doc COPYING
%{_includedir}/teamdctl.h
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteamdctl.pc

%files -n python-libteam
%doc COPYING _tmpdoc2/examples
%{python_sitearch}/*

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.11-3
- 为 Magic 3.0 重建

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1.11-2
- 为 Magic 3.0 重建

* Thu Jun 26 2014 Jiri Pirko <jpirko@redhat.com> - 1.11-1
- 1.11 release
- teamd: add forgotten teamd_link_watch.h to noinst_HEADERS
- teamd: add tipc.h kernel header
- teamd: Add support for TIPC link watcher
- teamd: add TIPC link watcher
- teamd: move icmp6 NS/NA ping link watcher to a separate file
- teamd: move arp ping link watcher to a separate file
- teamd: move psr template link watcher to a separate file
- teamd: move ethtool link watcher to a separate file
- teamd_dbus: add PortConfigDump to introspection
- teamd: allow restart on failure through systemd
- teamd: distinguish exit code between init error and runtime error
- man teamd.conf: remove "mandatory" since the options are no longer mandatory
- teamd: add "debug_level" config option
- teamd: allow to change debug level during run
- teamd: register debug callback at the start of callbacks list
- libteam: add team_change_handler_register_head function
- teamd: lacp: update partner info before setting state
- teamd: lacp: do not check SYNCHRO flag before enable of port
- teamd: lacp: "expired" port is not selectable, only "current"
- teamd: lacp: update actor system (mac) before sending lacpdu
- teamd: respect currently set user linkup for created linkwatches
- teamd: split --take-over option into --no-quit-destroy
- teamd: fix port removal when using take_over
- libteam: add SubmittingPatches doc
- libteam: Use u8 for put/get TEAM_ATTR_OPTION_TYPE

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Jiri Pirko <jpirko@redhat.com> - 1.10-1
- Update to 1.10
- teamd: quit when our team device is removed from outside
- libteam: ifinfo: watch for dellink messages and call change handlers for that
- initscripts: make ifup/ifdown scripts usable by ifup/ifdown-eth scripts
- teamdctl: unmess check_teamd_team_devname and fix double free there
- man: correct type of "*_host" options
- teamd_link_watch: specify "missed_max" option default value
- bond2team: do not guess source_host option
- teamd_link_watch: allow to send ARP probes if no source_host is specified
- initscripts: do not try to re-add port if it is already there
- teamdctl: add command for easy port presention checking
- Fix potential small memory leak
- usock: accept multiline message string parameters
- libteamdctl: add notice for caller to do not modify or free certain strings
- teamd: do not remove ports from team dev in case of take over mode
- teamd: look for existing ports before adding new ones
- libteam: introduce ream_refresh
- teamd: fixed couple comments.
- teamd: update hwaddr when changing team's macaddr
- redhat: fix boolean types in example 2
- initscripts: fix port up before master and port down after master
- lb: enable/disable port according to linkwatch state
- fix comment typo in ifdown-Team scripts
- man teamd.conf: Minor improvements to style and language
- man teamdctl: Minor improvements to style and language

* Thu Jan 23 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-2
- fix multilib

* Tue Nov 12 2013 Jiri Pirko <jpirko@redhat.com> - 1.9-1
- Update to 1.9
- libteamdctl: remove false lib dependencies
- teamdctl: use new port config get function
- libteamdctl: introduce support for port config get
- libteamdctl: cache reply strings into list
- teamd: introduce PortConfigDump control method
- teamd: make teamd_get_port_by_ifname ifname argument const
- Minor improvements to style and language.
- do not install example binaries
- minor man page(s) correction(s) and lintianisation
- teamdctl: print error message if ifindex cannot be obtained
- fix cflags path in pc files

* Tue Aug 13 2013 Jiri Pirko <jpirko@redhat.com> - 1.8-1
- Update to 1.8

* Mon Aug 12 2013 Jiri Pirko <jpirko@redhat.com> - 1.7-1
- Update to 1.7

* Thu Aug 08 2013 Jiri Pirko <jpirko@redhat.com> - 1.6-1
- Update to 1.6

* Tue Jul 30 2013 Jiri Pirko <jpirko@redhat.com> - 1.5-1
- Update to 1.5

* Tue Jun 11 2013 Jiri Pirko <jpirko@redhat.com> - 1.3-1
- Update to 1.3

* Wed May 29 2013 Jiri Pirko <jpirko@redhat.com> - 1.2-1
- Update to 1.2

* Thu May 16 2013 Jiri Pirko <jpirko@redhat.com> - 1.1-1
- Update to 1.1

* Thu Jan 31 2013 Jiri Pirko <jpirko@redhat.com> - 1.0-1
- Update to 1.0

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-27.20130110gitf16805c
- Rebuilt for libnl3

* Sun Jan 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.1-26.20130110gitf16805c
- Rebuilt for libnl3

* Thu Jan 10 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-25.20130110gitf16805c
- Rebase to git commit f16805c

* Wed Dec 12 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-24.20121212git01fe4bd
- Rebase to git commit 01fe4bd

* Thu Dec 06 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-23.20121206git659a848
- Rebase to git commit 659a848

* Thu Nov 22 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-22.20121122git18b6701
- Rebase to git commit 18b6701

* Thu Nov 15 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-21.20121115gitffb5267
- Rebase to git commit ffb5267

* Mon Nov 05 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-20.20121105git3b95b34
- Rebase to git commit 3b95b34

* Thu Oct 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-19.20121025git7fe7c72
- Rebase to git commit 7fe7c72

* Fri Oct 19 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-18.20121019git1a91059
- Rebase to git commit 1a91059

* Sun Oct 07 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-17.20121007git6f48751
- Rebase to git commit 6f48751

* Tue Sep 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-16.20120925gitcc5cddc
- Rebase to git commit cc5cddc

* Sun Sep 23 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-15.20120923git8448186
- Rebase to git commit 8448186

* Tue Sep 04 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-14.20120904gitbdcf72c
- Rebase to git commit bdcf72c

* Wed Aug 22 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-13.20120822gitc0d943d
- Rebase to git commit c0d943d

* Tue Aug 07 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-12.20120807git9fa4a96
- Rebase to git commit 9fa4a96

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-11.20120628gitca7b526
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-10.20120628gitca7b526
- Rebase to git commit ca7b526

* Wed Jun 27 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-9.20120627git96569f8
- Rebase to git commit 96569f8

* Wed Jun 27 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-8.20120627gitcd6b557
- Rebase to git commit cd6b557

* Wed Jun 20 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-7.20120620gita88fabf
- Rebase to git commit a88fabf

* Fri May 04 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-6.20120504git11e234a
- Rebase to git commit 11e234a

* Thu Apr 05 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-5.20120405gita82f8ac
- Rebase to git commit a82f8ac

* Tue Feb 21 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-4.20120221gitfe97f63
- Rebase to git commit fe97f63

* Mon Jan 30 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-3.20120130gitb5cf2a8
- Rebase to git commit b5cf2a8

* Wed Jan 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-2.20120125gita1718f8
- Rebase to git commit a1718f8

* Wed Jan 18 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-1.20120113git302672e
- Initial build.
