# TODO: uses private copy of libedit, should be modified to use system one

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Summary: IPMI (Intelligent Platform Management Interface) library and tools
Name: OpenIPMI
Version: 2.0.21
Release: 6%{?dist}
License: LGPLv2+ and GPLv2+ or BSD
Group: System Environment/Base
URL: http://sourceforge.net/projects/openipmi/
Source: http://downloads.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
Source1: openipmi.sysconf
Source2: openipmi-helper
Source3: ipmi.service
Source4: openipmi.modalias
BuildRequires: gdbm-devel swig glib2-devel net-snmp-devel ncurses-devel
BuildRequires: openssl-devel python-devel perl-devel tcl-devel tkinter
BuildRequires: desktop-file-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-sysv

Patch1: OpenIPMI-2.0.18-pthread-pkgconfig.patch
Patch2: OpenIPMI-2.0.19-man.patch
# switch from libedit bundle to system libedit
Patch3: OpenIPMI-2.0.21-nobundle.patch

%description
The Open IPMI project aims to develop an open code base to allow access to
platform information using Intelligent Platform Management Interface (IPMI).
This package contains the tools of the OpenIPMI project.

%package modalias
Group: System Environment/Kernel
Summary: Module aliases for IPMI subsystem
Requires: systemd
Requires: kmod

%description modalias
The OpenIPMI-modalias provides configuration file with module aliases
of ACPI and PNP wildcards.

%package libs
Group: Development/Libraries
Summary: The OpenIPMI runtime libraries

%description libs
The OpenIPMI-libs package contains the runtime libraries for shared binaries
and applications.

%package perl
Group: Development/Libraries
Summary: IPMI Perl language bindings
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
The OpenIPMI-perl package contains the Perl language bindings for OpenIPMI.

%package python
Group: Development/Libraries
Summary: IPMI Python language bindings

%description python
The OpenIPMI-python package contains the Python language bindings for OpenIPMI.

%package devel
Group: Development/Libraries
Summary: The development environment for the OpenIPMI project
Requires: pkgconfig
Requires: %{name} = %{version}-%{release}

%description devel
The OpenIPMI-devel package contains the development libraries and header files
of the OpenIPMI project.

%package lanserv
Summary: Emulates an IPMI network listener
Group: Utilities
Requires: %{name} = %{version}

%description lanserv
This package contains a network IPMI listener.


%prep
%setup -q
%patch1 -p1 -b .pthread
%patch2 -p1 -b .manscan
%patch3 -p1 -b .nobundle
rm -rf ./libedit

%build
export EDIT_CFLAGS=`pkg-config --cflags libedit`
export EDIT_LIBS=`pkg-config --libs libedit`
export CFLAGS="-fPIC $RPM_OPT_FLAGS -fno-strict-aliasing"

# aarch64 workaround remove once released package's config.sub contains aarch64
%{__libtoolize} --copy --force --automake
%{__aclocal}
%{__autoheader}
%{__automake} --add-missing --copy --foreign --force-missing
%{__autoconf}
# aarch64 end

%configure \
    --with-pythoninstall=%{python_sitearch} \
    --disable-dependency-tracking \
    --with-tcl=no \
    --disable-static \
    --with-tkinter=no

# https://fedoraproject.org/wiki/Packaging:Guidelines?rd=Packaging/Guidelines#Beware_of_Rpath
# get rid of rpath still present in OpenIPMI-perl package
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make   # not %{?_smp_mflags} safe

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/ipmi
install -d ${RPM_BUILD_ROOT}%{_libexecdir}
install -m 755 %SOURCE2 ${RPM_BUILD_ROOT}%{_libexecdir}/openipmi-helper
install -d ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_unitdir}/ipmi.service
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d
install -m 644 %SOURCE4 ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d/OpenIPMI.conf
install -d ${RPM_BUILD_ROOT}%{_localstatedir}/run/%{name}

rm ${RPM_BUILD_ROOT}/%{_mandir}/man1/openipmigui.1

# add missing documentation symlinks
if test -L ${RPM_BUILD_ROOT}/%{_bindir}/ipmicmd && ! test -a ${RPM_BUILD_ROOT}/%{_mandir}/man1/ipmicmd.1.gz ; then
    %{__ln_s} openipmicmd.1.gz ${RPM_BUILD_ROOT}/%{_mandir}/man1/ipmicmd.1.gz
fi

if test -L ${RPM_BUILD_ROOT}/%{_bindir}/ipmish && ! test -a ${RPM_BUILD_ROOT}/%{_mandir}/man1/ipmish.1.gz ; then
    %{__ln_s} openipmish.1.gz ${RPM_BUILD_ROOT}/%{_mandir}/man1/ipmish.1.gz
fi

%posttrans modalias
if [ -f "%{once}" ]; then
    if /usr/bin/udevadm info --export-db | grep -qie 'acpi:IPI0'; then
        /sbin/modprobe ipmi_si || :;
        /sbin/modprobe ipmi_devintf || :;
        /sbin/modprobe ipmi_msghandler || :;
        %{__rm} -f %{once} || :;
        /usr/bin/udevadm settle
    fi
fi
magic_rpm_clean.sh

%post modalias
if [ "$1" -eq 1 ]; then
    /bin/touch %{once}
fi

%post
%systemd_post ipmi.service

%preun
%systemd_preun ipmi.service

%postun
%systemd_postun_with_restart ipmi.service

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

### A sysv => systemd migration contains all of the same scriptlets as a
### systemd package.  These are additional scriptlets

%triggerun -- OpenIPMI < 2.0.18-14
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save ipmi >/dev/null 2>&1 ||:
/bin/systemctl --no-reload enable ipmi.service >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del ipmi >/dev/null 2>&1 || :
/bin/systemctl try-restart ipmi.service >/dev/null 2>&1 || :

%files
%doc CONFIGURING_FOR_LAN COPYING COPYING.BSD COPYING.LIB FAQ README README.Force README.MotorolaMXP
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%{_libexecdir}/openipmi-helper
%{_bindir}/ipmicmd
%{_bindir}/ipmilan
%{_bindir}/ipmish
%{_bindir}/ipmi_ui
%{_bindir}/openipmicmd
%{_bindir}/openipmish
%{_bindir}/rmcp_ping
%{_bindir}/solterm
%{_unitdir}/ipmi.service
%{_mandir}/man1/ipmi_ui*
%{_mandir}/man1/openipmicmd*
%{_mandir}/man1/openipmish*
%{_mandir}/man1/rmcp_ping*
%{_mandir}/man1/solterm*
%{_mandir}/man1/ipmish*
%{_mandir}/man1/ipmicmd*
%{_mandir}/man7/ipmi_cmdlang*
%{_mandir}/man7/openipmi_conparms*
%{_mandir}/man8/ipmilan*

%files perl
%attr(644,root,root) %{perl_vendorarch}/OpenIPMI.pm
%{perl_vendorarch}/auto/OpenIPMI/

%files python
%{python_sitearch}/*OpenIPMI*

%files libs
%{_libdir}/*.so.*

%files devel
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files lanserv
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ipmi/ipmisim1.emu
%config(noreplace) %{_sysconfdir}/ipmi/lan.conf
%{_bindir}/ipmilan
%{_bindir}/ipmi_sim
%{_bindir}/sdrcomp
%{_libdir}/libIPMIlanserv.so.*
%doc %{_mandir}/man8/ipmilan.8*
%doc %{_mandir}/man1/ipmi_sim.1*
%doc %{_mandir}/man5/ipmi_lan.5*
%doc %{_mandir}/man5/ipmi_sim_cmd.5*

%files modalias
%config(noreplace) %{_sysconfdir}/modprobe.d/OpenIPMI.conf
%{_localstatedir}/run/%{name}

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.0.21-6
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 2.0.21-5
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 2.0.21-4
- 为 Magic 3.0 重建

* Mon Mar 02 2015 Liu Di <liudidi@gmail.com> - 2.0.21-3
- 为 Magic 3.0 重建

* Mon Mar 02 2015 Liu Di <liudidi@gmail.com> - 2.0.21-2
- 为 Magic 3.0 重建

* Mon Mar 02 2015 Liu Di <liudidi@gmail.com> - 2.0.21-1
- 更新到 2.0.21

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.0.19-4
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.0.19-3
- 为 Magic 3.0 重建

* Mon Aug 27 2012 Jan Safranek <jsafrane@redhat.com> - 2.0.19-2
- Updated RPM scriptlets with latest systemd-rpm macros (#850246)
- Fixed fedora-review tool complaints

* Wed Aug  8 2012 Jan Safranek <jsafrane@redhat.com> - 2.0.19-1
- Update to 2.0.19

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.0.18-15
- Perl 5.16 rebuild

* Mon May  7 2012 Jan Safranek <jsafrane@redhat.com> - 2.0.18-14
- Added ipmi systemd unit

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.0.18-12
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.0.18-11
- Perl mass rebuild

* Fri Jul  8 2011 Jan Safranek <jsafrane@redhat.com> - 2.0.18-10
- Rebuilt for new Net-SNMP

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.18-9
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.18-8
- Perl 5.14 mass rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-6
- Removed the openipmigui tool, it does not work with TCL without thread
  support (#646184)

* Tue Oct 26 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-5
- Rebuilt for new Net-SNMP

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul  8 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-3
- added lincense files to OpenIPMI-libs subpackage as requested by
  Fedora Licensing Guidelines

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.0.18-2
- Mass rebuild with perl-5.12.0

* Wed May  5 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-1
- updated to OpenIPMI-2.0.18
- fixed OpenIPMIpthread pkgconfig file (#468067)

* Mon May  3 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.17-1
- updated to OpenIPMI-2.0.17

* Thu Mar 18 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-12
- implemented mandatory 'force-reload' command in ipmi service

* Thu Mar 11 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-11
- rebuild against new gdbm

* Wed Mar  3 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-10
- add README.initscript describing /etc/init.d/ipmi initscript exit codes
  (#562151)

* Mon Feb 22 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-9
- fix package License: field, there *are* sources with BSD header
- distribute README files and COPYING in package

* Tue Jan  5 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-8
- fix package License: field, there is no source with BSD header

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.0.16-7
- rebuild against perl 5.10.1

* Tue Dec  1 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-6
- fix package compilation to remove rpmlint errors

* Wed Sep 30 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-5
- rebuilt with new net-snmp

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.16-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 15 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-2
- fix compilation flags, debuginfo package is correctly generated now

* Thu Mar 19 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-1
- new upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.14-10
- rebuild with new openssl

* Thu Dec 11 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-9
- fix linking without rpath, prelink won't screw up the libraries
  anymore (#475265)

* Wed Dec 10 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-8
- shorter probe interval is used in init script, making the service startup
  quicker in most situations (#475101)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.14-7
- Rebuild for Python 2.6

* Thu Oct 30 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-6
- removed static libraries from the -devel subpackage
- fixed openipmigui.desktop file

* Thu Oct 23 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-5
- fixed typos in the descriptions
- added .desktop file for openipmigui tool

* Mon Oct 20 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-4
- fixed description of the package

* Thu Oct 16 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-3
- split ipmitool to separate package
- added 'reload' functionality to init script
- added seraparate -gui subpackage

* Wed Jul 30 2008 Phil Knirsch <pknirsch@redhat.com> - 2.0.14-2
- Fixed rpath problem in libOpenIPMIposix.so.0.0.1

* Tue Jul 29 2008 Phil Knirsch <pknirsch@redhat.com> - 2.0.14-1
- Fixed several specfile problems (#453751)
- Update to OpenIPMI-2.0.14

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.13-2
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.13-1
- Updated to OpenIPMI-2.0.13
- Rebuild due to new openssl

* Wed Oct 10 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-3
- Added missing perl-devel buildrequires

* Mon Sep 24 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-2
- Added missing popt-devel buildrequires

* Fri Aug 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-2
- Fix rebuild problems due to glibc change
- License review and fixes

* Tue Apr 24 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-1
- Update to OpenIPMI-2.0.11

* Tue Feb 27 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-8
- Update for ipmitool-1.8.9

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.0.6-7
- rebuild for python 2.5

* Tue Nov 28 2006 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-6.fc7
- Update due to new net-snmp-5.4
- Some specfile updates

* Tue Jul 18 2006 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-5
- Fixed check for udev in initscript (#197956)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.6-4.1
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com> 2.0.6-4
- don't include <linux/compiler.h>

* Fri Jun 16 2006 Jon Masters <jcm@redhat.com> 2.0.6-3
- Fix a build requires (needs glibc-kernheaders)

* Thu Jun 15 2006 Jesse Keating <jkeating@redhat.com> 2.0.6-2
- Bump for new glib2

* Tue May 16 2006 Phil Knirsch <pknirsch@redhat.com> 2.0.6-1
- Fixed bug with type conversion in ipmitool (#191091)
- Added python bindings 
- Split off perl and python bindings in separate subpackages
- Dropped obsolete patches
- Added missing buildprereq on readline-devel
- Made it install the python bindings properly on 64bit archs

* Mon May 15 2006 Phil Knirsch <pknirsch@redhat.com>
- Updated ipmitool to 1.8.8
- Updated OpenIPMI to 2.0.6

* Fri Feb 17 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-19
- Added missing PreReq for chkconfig

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-18
- Updated ipmitool to latest upstream version.
- Removed 3 patches for already fixed bugs in latest ipmitool.
- Adapted warning message fix for ipmitool for latest version.

* Tue Jan 24 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-17
- Fixed some minor things in initscripts.

* Mon Jan 09 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-16
- Included FRU fix for displaying FRUs with ipmitool
- Included patch for new option to specify a BMC password for IPMI 2.0 sessions

* Tue Jan 03 2006 Radek Vokal <rvokal@redhat.com> 1.4.14-15
- Rebuilt against new libnetsnmp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-14
- Some more initscript and sysconfig updates from Dell.

* Wed Nov 09 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-13
- Rebuilt to link against latest openssl libs.
- Fixed ipmitool not setting session privilege level (#172312)

* Wed Nov 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-11
- Rebuild to link against new net-snmp libs.

* Tue Oct 11 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-10
- Updated initscript to fix missing redhat-lsb bug (#169901)

* Thu Sep 08 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-9
- Another update to latest initscripts from Dell
- Fixed some missing return statements for non-void functions (#164138)

* Thu Sep 01 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-8
- Updated initscript to latest version from Dell

* Fri Aug 12 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-7
- Fixed the unwanted output of failed module loading of the initscript. Behaves
  now like all our other initscripts (#165476)

* Fri Aug 05 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-6
- Fixed build problem on 64bit machines

* Fri Jul 15 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-5
- Fixed missing change to not autostart in the initscript

* Wed Jul 06 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-4
- Made the initscript a replacing configfile

* Mon Jul 04 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-3
- Updated versions of the initscripts and sysconf files
- Fixed typo in preun script and changelog

* Mon Jun 27 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-2
- Updated to OpenIPMI-1.4.14
- Split the main package into normal and libs package for multilib support
- Added ipmitool-1.8.2 to OpenIPMI and put it in tools package
- Added sysconf and initscript (#158270)
- Fixed oob subscripts (#149142)

* Wed Mar 30 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-5
- Correctly put libs in the proper packages

* Thu Mar 17 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-4
- gcc4 rebuild fixes
- Added missing gdbm-devel buildprereq

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-3
- bump release and rebuild with gcc 4

* Tue Feb 08 2005 Karsten Hopp <karsten@redhat.de> 1.4.11-2 
- update

* Tue Oct 26 2004 Phil Knirsch <pknirsch@redhat.com>
- Initial version
