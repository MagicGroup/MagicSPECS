Name: lm_sensors
Version:	3.3.5
Release: 2%{?dist}
URL: http://www.lm-sensors.org/
Source: http://dl.lm-sensors.org/lm-sensors/releases/%{name}-%{version}.tar.bz2
Source1: lm_sensors.sysconfig
# these 2 were taken from PLD-linux, Thanks!
Source2: sensord.sysconfig
Source3: sensord.init
Summary: Hardware monitoring tools
Group: Applications/System
License: LGPLv2+
%ifarch %{ix86} x86_64
Requires: /usr/sbin/dmidecode
%endif
Requires(post): systemd-units
BuildRequires: kernel-headers >= 2.2.16, bison, libsysfs-devel, flex, gawk
BuildRequires: rrdtool-devel

%description
The lm_sensors package includes a collection of modules for general SMBus
access and hardware monitoring.


%package libs
Summary: Lm_sensors core libraries
Group: System Environment/Libraries

%description libs
Core libraries for lm_sensors applications


%package devel
Summary: Development files for programs which will use lm_sensors
Group: Development/System
Requires: %{name}-libs = %{version}-%{release}

%description devel
The lm_sensors-devel package includes a header files and libraries for use
when building applications that make use of sensor data.


%package sensord
Summary: Daemon that periodically logs sensor readings
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description sensord
Daemon that periodically logs sensor readings to syslog or a round-robin
database, and warns of sensor alarms.


%prep
%setup -q

mv prog/init/README prog/init/README.initscripts
chmod -x prog/init/fancontrol.init


%build
export CFLAGS="%{optflags}"
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} EXLDFLAGS= \
  PROG_EXTRA=sensord user


%install
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} PROG_EXTRA=sensord \
  DESTDIR=$RPM_BUILD_ROOT user_install
rm $RPM_BUILD_ROOT%{_libdir}/libsensors.a

ln -s sensors.conf.5.gz $RPM_BUILD_ROOT%{_mandir}/man5/sensors3.conf.5.gz

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sensors.d
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lm_sensors
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sensord
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/sensord
install -p -m 644 prog/init/lm_sensors.service \
    $RPM_BUILD_ROOT/lib/systemd/system


# Note non standard systemd scriptlets, since reload / stop makes no sense
# for lm_sensors
%triggerun -- lm_sensors < 3.3.0-2
if [ -L /etc/rc3.d/S26lm_sensors ]; then
    /bin/systemctl enable lm_sensors.service >/dev/null 2>&1 || :
fi
/sbin/chkconfig --del lm_sensors

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable lm_sensors.service > /dev/null 2>&1 || :
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post sensord
/sbin/chkconfig --add sensord

%preun sensord
if [ $1 = 0 ]; then
    /sbin/chkconfig --del sensord
fi


%files
%defattr(-,root,root,-)
%doc CHANGES CONTRIBUTORS COPYING doc README*
%doc prog/init/fancontrol.init prog/init/README.initscripts
%config(noreplace) %{_sysconfdir}/sensors3.conf
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/*
/lib/systemd/system/lm_sensors.service
%config(noreplace) %{_sysconfdir}/sysconfig/lm_sensors
%exclude %{_sbindir}/sensord
%exclude %{_mandir}/man8/sensord.8.gz
%dir %{_sysconfdir}/sensors.d

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/sensors
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files sensord
%defattr(-,root,root,-)
%doc prog/sensord/README
%{_sbindir}/sensord
%{_mandir}/man8/sensord.8.gz
%{_initrddir}/sensord
%config(noreplace) %{_sysconfdir}/sysconfig/sensord


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 3.3.5-2
- 为 Magic 3.0 重建

* Thu Jul 03 2014 Liu Di <liudidi@gmail.com> - 3.3.5-1
- 更新到 3.3.5

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.3.1-2
- 为 Magic 3.0 重建

* Fri Jul 22 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.1-1
- new upstream release 3.3.1

* Sun Apr 24 2011 Hans de Goede <hdegoede@redhat.com> - 3.3.0-2
- Fix sensors-detect with the udevdb now living under /run (#697565)
- Provide a native systemd service file (#692159)
- Drop systemv initscript
- Drop configuration conversion scripts, the last Fedora with lm_sensors-2.x
  was Fedora 8 ! 

* Tue Mar 29 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.0
- new upstream release 3.3.0
- Resolved: 691548 - include empty /etc/sensors.d into the package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.2.0
- new upstream release 3.2.0
- change lincese to LGPLv2.1

* Fri Sep 03 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.2.svn5857
- update lm_sensors from svn
- drop patch lm_sensors-3.1.2-lm85.patch(already in svn)

* Wed Mar 31 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.2-2
- patch lm_sensors-3.1.2-lm85.patch add into sensors-detect driver lm85
- Resolved: 578527 - sensors-detect fails to detect

* Wed Feb 3 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.2-1
- new upstream release
- drop sensors-detect, beacuse it was taken form svn(531126)

* Thu Dec 17 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.1-7
- Resovles: #226101 - Merge Review: lm_sensors

* Tue Nov 10 2009 Dennis Gilmore <dennis@ausil.us> - 3.1.1-6
- remove Excludearch s390 s390x

* Tue Nov 10 2009 Nikola Pajkovsky <n.pajkovsky@gmail.com> - 3.1.1-5
- Resolved: 531126 - sensors-detect gives perl uninitialized var warnings

* Wed Sep 30 2009 Hans de Goede <hdegoede@redhat.com> 3.1.1-4
- Create a sensor3.conf.5 symlink to the sensors.conf.5 manpage (#526178)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Adam Jackson <ajax@redhat.com> 3.1.1-2
- Add -libs subpackage so perl doesn't get dragged in just for linking
  against libsensors.

* Tue Jul  7 2009 Nikola Pajokvsky <npajovs@redhat.com> 3.1.1-1
- New release 3.1.1

* Sun Mar  8 2009 Hans de Goede <hdegoede@redhat.com> 3.1.0-1
- New upstream release 3.1.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan  1 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.3-1
- New upstream release 3.0.3
- Add a patch to support drivers with an ACPI "bus" (new Asus atk0110 drv)

* Tue Jul  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.2-1
- New upstream release 3.0.2
- This release contains various important fixes to sensors-detect, which made
  it unsafe to run sensors-detect on certain systems
- Drop all patches (all upstreamed)

* Sat Jun 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-6
- Rebuild for new rrdtool

* Sun Mar 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-5
- Make libsensors work with hwmon class entries without a device link
  such as the acpi thermal_zone driver (bz 437637)

* Wed Mar 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-4
- One (last) minor cosmetical fix to the initscript

* Tue Feb 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-3
- Some improvements to the lsb-retcodes and service-default-off patches
  from a review by upstream

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.1-2
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-1
- New upstream release 3.0.1
- Drop several patches which are included in the new upstream release
- Add a patch to make the initscript returncodes LSB compliant (bug 431884)

* Tue Dec 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-3
- Fix sensors.conf errors with certain chips (patch send in by upstream)

* Thu Dec 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-2
- Fix sensord rdd mode (patch send in by upstream)

* Sat Nov 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-1
- New upstream release 3.0.0 (final)

* Sat Nov 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 3.0.0-0.1.rc3
- New upstream release 3.0.0-rc3
- Remove eeprommer sub-package as eeprommer (and the other i2c-tools)
  have moved to the new i2c-tools package

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.10.4-2
- Update License tag for new Licensing Guidelines compliance
- Disable service by default (no use without any sensors being configured),
  enable it automatically on a successfull sensors-detect run (bz 253750)

* Thu Jul 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.10.4-1
- New upstream release 2.10.4
- Drop upstreamed patches 4, 5, 7 and 8
- Drop no longer need patch 3
- Move libsensors.3 manpage to -devel sub-package
- Move sensord.8 manpage to -sensord sub-package
- Switch from ExclusiveArch: alph ix86 x86_64, to ExcludeArch: s390 s390x,
  so that we get build on ppc, arm, etc. too. (bz 181037 amongst others)

* Mon Jul  9 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.10.3-3
- Remove no longer needed patches 1, 2 & 6
- Various specfile cleanups to match the Fedora packaging guidelines
  this fixes bz 238787 amongst other things
- Use lm_sensors provided initscript instead of our own private one, this
  stops the sometimes unnecessary loading of i2c-dev
- No longer ship a static version of the library in -devel
- Compile sensord and eepromer extra programs and put each in its own
  subpackage (bz 236904)

* Tue Apr 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.3-2
- Fixed one more problem with sensors-detect (#215984)

* Tue Apr 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.3-1
- Update to lm_sensors-2.10.3

* Thu Mar 15 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.2-2
- Only require dmidecode on supported archs (#232264)

* Tue Feb 06 2007 Florian La Roche <laroche@redhat.com> - 2.10.2-1
- Update to lm_sensors-2.10.2

* Thu Nov 23 2006 Phil Knirsch <pknirsch@redhat.com> - 2.10.1-1.fc7
- Update to lm_sensors-2.10.1
- Tiny specfile updates

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.10.0-3.1
- rebuild

* Sun Jul 09 2006 Warren Togami <wtogami@redhat.com> 2.10.0-3
- change buildreq from sysfsutils-devel to libsysfs-devel (#198055)

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> 2.10.0-2
- Fix BuildRequires, added flex. (#193511)  Changed to Requires(post) and 
  (postun)

* Fri May 12 2006 Phil Knirsch <pknirsch@redhat.com> 2.10.0-1
- Update to lm_sensors-2.10.0
- Added missing buildprereq on sysfsutils-devel (#189196)
- Added missing prereq on chkconfig (#182838)
- Some fiddling to make it build on latest kernels

* Wed Feb 15 2006 Phil Knirsch <pknirsch@redhat.com> 2.9.2-2
- Added missing dependency to chkconfig

* Fri Feb 10 2006 Phil Knirsch <pknirsch@redhat.com> 2.9.2-1
- Update to lm_sensors-2.9.2
- Fixed wrong subsys locking (#176965)
- Removed lm_sensors pwmconfig, has been fixed upstream now

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.9.1-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Peter Jones <pjones@redhat.com> 2.9.1-6
- fix initscript subsys locking

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com> 2.9.1-5.1
- rebuilt for new gcj

* Tue Nov 08 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.1-5
- Fixed lm_sensors pwmconfig patch.

* Tue Sep 01 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.1-4
- Fixed CAN-2005-2672 lm_sensors pwmconfig insecure temporary file usage
  (#166673)
- Fixed missing optflags during build (#166910)

* Mon May 23 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.1-3
- Update to lm_sensors-2.9.1
- Fixed wrong/missing location variables for make user
- Fixed missing check for /etc/modprobe.conf in sensors-detect (#139245)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 2.8.8-5
- bump release and rebuild with gcc 4

* Tue Jan 11 2005 Dave Jones <davej@redhat.com> 2.8.8-4
- Add dependancy on dmidecode rather than the obsolete kernel-utils.
- Don't delete dmidecode from the buildroot.

* Thu Dec 23 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.8-2
- Fixed typo in initscript (#139030)

* Tue Dec 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.8-1
- Added Buildprereq for bison (#138888)
- Update to lm_sensors-2.8.8

* Thu Oct 14 2004 Harald Hoyer <harald@redhat.com> 2.8.7-2
- added initial /etc/sysconfig/lm_sensors
- added initscript
- MAKEDEV the initial i2c devices in initscript and sensors-detect

* Tue Jul 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.7-1
- Update to latest upstream version.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.6-1
- Update to latest upstream version.
- Enabled build for x86_64.

* Mon Mar 08 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-5
- Fixed initscript to work with 2.6 kernel and made it more quiet (#112286).
- Changed proposed location of sensors (#116496).
- Fixed rpath issue.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-3
- Modified sensors.conf to a noreplace config file.

* Wed Feb 04 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-2
- Fixed newly included initscript (#114608).

* Thu Jan 29 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-1
- Updated to latest upstream version 2.8.3

* Thu Jan 08 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.2-1
- Update to latest upstream version 2.8.2
- Fixed wrong & usage in if expression.
- Included several new perl tools.

* Fri Oct 24 2003 Phil Knirsch <pknirsch@redhat.com> 2.8.1-1
- Update to latest upstream version 2.8.1

* Wed Jul 23 2003 Phil Knirsch <pknirsch@redhat.com> 2.8.0-1
- Update to latest upstream version 2.8.0

* Fri Jun 27 2003 Phil Knirsch <pknirsch@redhat.com> 2.6.5-6.1
- rebuilt

* Fri Jun 27 2003 Phil Knirsch <pknirsch@redhat.com> 2.6.5-6
- Included prog/init scripts and README (#90606).
- Require kernel-utils for dmidecode (#88367, #65057).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.6.5-5
- rebuilt

* Wed Dec 04 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.5-4
- Bump release and try to rebuild.

* Tue Dec  3 2002 Tim Powers <timp@redhat.com> 2.6.5-3
- don't include dmidecode, conflicts with kernel-utils

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.5-2
- Added patch to fix utf8 problem with sensors-detect.
- Fixed Copyright: to License: in specfile

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.5-1
- Updated userlevel to 2.6.5.
- Include all the /usr/sbin/ apps (like dmidecode).

* Fri Oct 04 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.3-3
- Removed Serverworks patch as it is already in sensors-detect.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.6.3-2
- automated rebuild

* Tue Jun 18 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.3-1
- Updated of userland package to 2.6.3
- Fixed file packaging bug (#66126).

* Thu May 23 2002 Tim Powers <timp@redhat.com> 2.6.2-2
- automated rebuild

* Mon Jan 28 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.2-1
- Update to version 2.6.2

* Wed Aug 22 2001 Philipp Knirsch <pknirsch@redhat.de> 2.5.5-6
- Added the SMBus CSB5 detection (#50468)

* Mon Jul  9 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed duplicate Summary: entry for devel package (#47714)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Feb 15 2001 Philipp Knirsch <pknirsch@redhat.de>
- Removed the i2c block patch as our newest kernel doesn't need it anymore.

* Mon Feb  5 2001 Matt Wilson <msw@redhat.com>
- added patch to not include sys/perm.h, as it's gone now.
- added alpha to ExclusiveArch
- use make "LINUX_HEADERS=/usr/include" to get kernel headers

* Tue Jan 16 2001 Philipp Knirsch <pknirsch@redhat.de>
- Updated to 2.5.5 which includes the Serverworks drivers. Kernel modules are
  not included though es they have to go into the kernel package
- Had to remove all references to I2C_SMBUS_I2C_BLOCK_DATA from
  kernel/busses/i2c-i801.c and prog/dump/i2cdump.c as this is not defined in
  our current kernel package

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- update to 2.5.4
- updated URL and Source entries to point to new home of lm-sensors
- rebuild

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summary

* Fri Jul 28 2000 Harald Hoyer <harald@redhat.de>
- added static library to devel package

* Thu Jul 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2
- build against a kernel that actually has new i2c code in it

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- initial package without kernel support
