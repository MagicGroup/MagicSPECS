%global _hardened_build 1

Summary: Bluetooth utilities
Name: bluez
Version: 5.35
Release: 2%{?dist}
License: GPLv2+
Group: Applications/System
URL: http://www.bluez.org/

Source0: http://www.kernel.org/pub/linux/bluetooth/bluez-%{version}.tar.xz
Source1: bluez.gitignore

## Ubuntu patches
Patch2: 0001-work-around-Logitech-diNovo-Edge-keyboard-firmware-i.patch
# Non-upstream
Patch3: 0001-Allow-using-obexd-without-systemd-in-the-user-sessio.patch
Patch4: 0001-obex-Use-GLib-helper-function-to-manipulate-paths.patch
Patch5: 0002-autopair-Don-t-handle-the-iCade.patch
Patch7: 0004-agent-Assert-possible-infinite-loop.patch

BuildRequires: git
BuildRequires: dbus-devel >= 0.90
BuildRequires: glib2-devel
BuildRequires: libical-devel
BuildRequires: readline-devel
# For cable pairing
BuildRequires: systemd-devel
# For cups
BuildRequires: cups-devel

# For rebuild
BuildRequires: libtool autoconf automake

Requires: dbus >= 0.60

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# Dropped in Fedora 20:
Obsoletes: bluez-alsa < 5.0
Obsoletes: bluez-compat < 5.0
Obsoletes: bluez-gstreamer < 5.0

# Other bluetooth-releated packages that haven't gotten ported to BlueZ 5
Obsoletes: blueman < 1.23-9
Obsoletes: blueman-nautilus < 1.23-9
Obsoletes: obex-data-server < 1:0.4.6-8

%description
Utilities for use in Bluetooth applications:
	- hcitool
	- hciattach
	- hciconfig
	- bluetoothd
	- l2ping
	- rfcomm
	- sdptool
	- bccmd
	- bluetoothctl
	- btmon
	- hcidump
	- l2test
	- rctest
	- start scripts (Red Hat)
	- pcmcia configuration files

The BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package libs
Summary: Libraries for use in Bluetooth applications
Group: System Environment/Libraries

%package libs-devel
Summary: Development libraries for Bluetooth applications
Group: Development/Libraries
Requires: bluez-libs%{?_isa} = %{version}-%{release}

%package cups
Summary: CUPS printer backend for Bluetooth printers
Group: System Environment/Daemons
Requires: bluez%{?_isa} = %{version}-%{release}
Requires: cups

%package hid2hci
Summary: Put HID proxying bluetooth HCI's into HCI mode
Group: System Environment/Daemons
Requires: bluez%{?_isa} = %{version}-%{release}

%description cups
This package contains the CUPS backend

%description libs
Libraries for use in Bluetooth applications.

%description libs-devel
bluez-libs-devel contains development libraries and headers for
use in Bluetooth applications.

%description hid2hci
Most allinone PC's and bluetooth keyboard / mouse sets which include a
bluetooth dongle, ship with a so called HID proxying bluetooth HCI.
The HID proxying makes the keyboard / mouse show up as regular USB HID
devices (after connecting using the connect button on the device + keyboard),
which makes them work without requiring any manual configuration.

The bluez-hid2hci package contains the hid2hci utility and udev rules to
automatically switch supported Bluetooth devices into regular HCI mode.

Install this package if you want to use the bluetooth function of the HCI
with other bluetooth devices like for example a mobile phone.

Note that after installing this package you will first need to pair your
bluetooth keyboard and mouse with the bluetooth adapter before you can use
them again. Since you cannot use your bluetooth keyboard and mouse until
they are paired, this will require the use of a regular (wired) USB keyboard
and mouse.

%prep
%setup -q
git init
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "bluez-owner@fedoraproject.org"
    git config user.name "Fedora Bluez maintainers"
fi
cp %{SOURCE1} .gitignore
git add .
git commit -a -q -m "%{version} baseline."

git am -p1 %{patches} < /dev/null

%build
libtoolize -f -c
autoreconf -f -i
%configure --enable-cups --enable-tools --enable-library \
           --enable-sixaxis \
           --with-systemdsystemunitdir=%{_unitdir} \
           --with-systemduserunitdir=%{_userunitdir}
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove autocrap and libtool droppings
find $RPM_BUILD_ROOT -name '*.la' -delete

# Remove the cups backend from libdir, and install it in /usr/lib whatever the install
if test -d ${RPM_BUILD_ROOT}/usr/lib64/cups ; then
	install -D -m0755 ${RPM_BUILD_ROOT}/usr/lib64/cups/backend/bluetooth ${RPM_BUILD_ROOT}%_cups_serverbin/backend/bluetooth
	rm -rf ${RPM_BUILD_ROOT}%{_libdir}/cups
fi

rm -f ${RPM_BUILD_ROOT}/%{_sysconfdir}/udev/*.rules ${RPM_BUILD_ROOT}/usr/lib/udev/rules.d/*.rules
install -D -p -m0644 tools/hid2hci.rules ${RPM_BUILD_ROOT}/lib/udev/rules.d/97-hid2hci.rules

install -d -m0755 $RPM_BUILD_ROOT/%{_localstatedir}/lib/bluetooth

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/bluetooth/

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post
%systemd_post bluetooth.service

%preun
%systemd_preun bluetooth.service

%postun
%systemd_postun_with_restart bluetooth.service

%post hid2hci
/sbin/udevadm trigger --subsystem-match=usb

%files
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/ciptool
%{_bindir}/hcitool
%{_bindir}/l2ping
%{_bindir}/rfcomm
%{_bindir}/sdptool
%{_bindir}/bccmd
%{_bindir}/bluetoothctl
%{_bindir}/bluemoon
%{_bindir}/btmon
%{_bindir}/hciattach
%{_bindir}/hciconfig
%{_bindir}/hcidump
%{_bindir}/l2test
%{_bindir}/rctest
%{_bindir}/hex2hcd
%{_bindir}/mpris-proxy
%{_mandir}/man1/ciptool.1.gz
%{_mandir}/man1/hcitool.1.gz
%{_mandir}/man1/rfcomm.1.gz
%{_mandir}/man1/sdptool.1.gz
%{_mandir}/man1/bccmd.1.*
%{_mandir}/man1/hciattach.1.*
%{_mandir}/man1/hciconfig.1.*
%{_mandir}/man1/hcidump.1.*
%{_mandir}/man1/l2ping.1.*
%{_mandir}/man1/rctest.1.*
%{_mandir}/man8/*
%{_libexecdir}/bluetooth/bluetoothd
%{_libexecdir}/bluetooth/obexd
%exclude %{_mandir}/man1/hid2hci.1*
%config %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%{_libdir}/bluetooth/
%{_localstatedir}/lib/bluetooth
%{_datadir}/dbus-1/system-services/org.bluez.service
%{_datadir}/dbus-1/services/org.bluez.obex.service
%{_unitdir}/bluetooth.service
%{_userunitdir}/obex.service

%files libs
%doc COPYING
%{_libdir}/libbluetooth.so.*

%files libs-devel
%{_libdir}/libbluetooth.so
%dir %{_includedir}/bluetooth
%{_includedir}/bluetooth/*
%{_libdir}/pkgconfig/bluez.pc

%files cups
%_cups_serverbin/backend/bluetooth

%files hid2hci
/usr/lib/udev/hid2hci
%{_mandir}/man1/hid2hci.1*
/lib/udev/rules.d/97-hid2hci.rules

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 5.35-2
- 更新到 5.35

* Mon Feb 16 2015 Liu Di <liudidi@gmail.com> - 5.28-1
- 更新到 5.28

* Fri Jul 25 2014 Liu Di <liudidi@gmail.com> - 5.21-1
- 更新到 5.21

* Wed Mar 05 2014 Liu Di <liudidi@gmail.com> - 5.15-1
- 更新到 5.15

* Wed Jan 29 2014 Bastien Nocera <bnocera@redhat.com> 5.14-1
- Update to 5.14

* Mon Jan 06 2014 Bastien Nocera <bnocera@redhat.com> 5.13-1
- Update to 5.13
- Enable sixaxis plugin by default

* Thu Dec 12 2013 Bastien Nocera <bnocera@redhat.com> 5.12-2
- This update fixes Sixaxis PS3 joypad detection

* Wed Dec 11 2013 Bastien Nocera <bnocera@redhat.com> 5.12-1
- Update to 5.12
- Sixaxis PS3 joypad support is now upstream

* Tue Dec 10 2013 Bastien Nocera <bnocera@redhat.com> 5.11-2
- Add crasher fixes (rhbz #1027365)

* Mon Nov 18 2013 Bastien Nocera <bnocera@redhat.com> 5.11-1
- Update to 5.11

* Tue Nov 12 2013 Bastien Nocera <bnocera@redhat.com> 5.10-4
- Default to the XDG cache dir for receiving files

* Mon Oct 21 2013 Bastien Nocera <bnocera@redhat.com> 5.10-3
- Remove a few obsolete BRs and deps, thanks to Marcel Holtmann

* Mon Oct 21 2013 Bastien Nocera <bnocera@redhat.com> 5.10-2
- Add non-upstreamable patch to make bluetooth-sendto work again

* Thu Oct 17 2013 Bastien Nocera <bnocera@redhat.com> 5.10-1
- Update to 5.10

* Fri Sep 20 2013 Kalev Lember <kalevlember@gmail.com> 5.9-4
- Obsolete blueman-nautilus as well

* Fri Sep 20 2013 Kalev Lember <kalevlember@gmail.com> 5.9-3
- Obsolete blueman and obex-data-server

* Fri Sep 20 2013 Bastien Nocera <bnocera@redhat.com> 5.9-2
- Fix problem unsetting discoverable

* Fri Sep 20 2013 Bastien Nocera <bnocera@redhat.com> 5.9-1
- Update to 5.9

* Fri Aug 16 2013 Kalev Lember <kalevlember@gmail.com> - 5.8-2
- Don't pull in -libs for the other subpackages
- Remove a stray .la file

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 5.8-1
- Update to 5.8
- Hardened build
- Use systemd rpm macros

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 5.5-1
- Update to 5.5, based on earlier work from
  https://bugzilla.redhat.com/show_bug.cgi?id=974145

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.101-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Bastien Nocera <bnocera@redhat.com> 4.101-9
- Fix trust setting in Sixaxis devices

* Wed Jun 26 2013 Bastien Nocera <bnocera@redhat.com> 4.101-8
- Another pass at fixing A2DP support (#964031)

* Tue Jun 25 2013 Bastien Nocera <bnocera@redhat.com> 4.101-7
- Remove socket interface enablement for A2DP (#964031)

* Mon Jan 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.101-6
- Add -vif to autoreconf to fix build issues

* Thu Jan 10 2013 Bastien Nocera <bnocera@redhat.com> 4.101-5
- Use git to manage distro patches
- Add numerous upstream and downstream patches (#892929)

* Wed Nov 21 2012 Bastien Nocera <bnocera@redhat.com> 4.101-4
- Clean up requires and build requires
- Use CUPS macro (#772236)
- Enable audio socket so a2dp works in PulseAudio again (#874015)
- Fix hid2hci not working with recent kernels (#877998)

* Wed Aug 15 2012 Bastien Nocera <bnocera@redhat.com> 4.101-3
- Enable pairing Wiimote support (#847481)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Bastien Nocera <bnocera@redhat.com> 4.100-2
- Add PS3 BD Remote patches (power saving)

* Thu Jun 14 2012 Bastien Nocera <bnocera@redhat.com> 4.100-1
- Update to 4.100

* Fri Jun  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 4.99-2
- Add patch for udev change to fix FTBFS on rawhide
- Drop sbc patch as fixed in gcc 4.7 final

* Tue Mar 06 2012 Bastien Nocera <bnocera@redhat.com> 4.99-1
- Update to 4.99

* Tue Feb 28 2012 Petr Pisar <ppisar@redhat.com> - 4.98-3
- Make headers compilable with g++ 4.7 (bug #791292)

* Fri Feb 24 2012 Peter Robinson <pbrobinson@fedoraproject.org> 4.98-2
- Add mmx patch to fix build of sbc component
- clean up spec, drop ancient obsoletes

* Fri Jan 13 2012 Bastien Nocera <bnocera@redhat.com> 4.98-1
- Update to 4.98

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Bastien Nocera <bnocera@redhat.com> 4.97-1
- Update to 4.97

* Mon Sep  5 2011 Hans de Goede <hdegoede@redhat.com> 4.96-3
- Put hid2hci into its own (optional) subpackage, so that people who
  just want to use their HID proxying HCI with the keyboard and mouse
  it came with, will have things working out of the box.
- Put udev rules in /lib/udev, where package installed udev rules belong

* Mon Aug 29 2011 Hans de Goede <hdegoede@redhat.com> 4.96-2
- hid2hci was recently removed from udev and added to bluez in 4.93,
  udev in Fedora-16 no longer has hid2hci -> enable it in our bluez builds.
  This fixes bluetooth not working on machines where the bluetooth hci
  initially shows up as a hid device, such as with many Dell laptops.

* Mon Aug 01 2011 Bastien Nocera <bnocera@redhat.com> 4.96-1
- Update to 4.96

* Tue Jul 05 2011 Bastien Nocera <bnocera@redhat.com> 4.95-1
- Update to 4.95

* Tue Jun 28 2011 Lennart Poettering <lpoetter@redhat.com> - 4.94-4
- Enable bluetoothd on all upgrades from 4.87-6 and older, in order to fix up broken F15 installations

* Thu Jun 23 2011 Bastien Nocera <bnocera@redhat.com> 4.94-3
- Update patches to apply correctly
- First compilable version with hostnamed support

* Mon Jun 20 2011 Lennart Poettering <lpoetter@redhat.com> - 4.94-2
- Enable bluetoothd by default
- Follow-up on https://bugzilla.redhat.com/show_bug.cgi?id=694519 also fixing upgrades

* Wed Jun 01 2011 Bastien Nocera <bnocera@redhat.com> 4.94-1
- Update to 4.94

* Wed May 25 2011 Bastien Nocera <bnocera@redhat.com> 4.93-1
- Update to 4.93

* Thu Apr  7 2011 Lennart Poettering <lpoetter@redhat.com> - 4.90-2
- Update systemd patch to make it possible to disable bluez

* Thu Mar 17 2011 Bastien Nocera <bnocera@redhat.com> 4.90-1
- Update to 4.90

* Mon Feb 21 2011 Bastien Nocera <bnocera@redhat.com> 4.89-1
- Update to 4.89

* Mon Feb 14 2011 Bastien Nocera <bnocera@redhat.com> 4.88-1
- Update to 4.88

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Bastien Nocera <bnocera@redhat.com> 4.87-1
- Update to 4.87

* Thu Jan 20 2011 Bastien Nocera <bnocera@redhat.com> 4.86-1
- Update to 4.86

* Thu Jan 13 2011 Bastien Nocera <bnocera@redhat.com> 4.85-1
- Update to 4.85

* Sun Dec 19 2010 Bastien Nocera <bnocera@redhat.com> 4.82-1
- Update to 4.82

* Wed Dec 01 2010 Bastien Nocera <bnocera@redhat.com> 4.81-1
- Update to 4.81

* Mon Nov 22 2010 Bastien Nocera <bnocera@redhat.com> 4.80-1
- Update to 4.80

* Tue Nov 09 2010 Bastien Nocera <bnocera@redhat.com> 4.79-1
- Update to 4.79

* Sat Nov 06 2010 Bastien Nocera <bnocera@redhat.com> 4.78-1
- Update to 4.78

* Wed Oct 27 2010 Bastien Nocera <bnocera@redhat.com> 4.77-1
- Update to 4.77

* Sat Oct 16 2010 Bastien Nocera <bnocera@redhat.com> 4.76-1
- Update to 4.76

* Tue Oct 05 2010 Bastien Nocera <bnocera@redhat.com> 4.74-1
- Update to 4.74

* Mon Oct 04 2010 Bastien Nocera <bnocera@redhat.com> 4.73-1
- Update to 4.73

* Wed Sep 29 2010 jkeating - 4.72-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Bastien Nocera <bnocera@redhat.com> 4.72-1
- Update to 4.72

* Fri Sep 17 2010 Bill Nottingham <notting@redhat.com> 4.71-4
- sync release number (but not package) with F-14

* Tue Sep 14 2010 Bastien Nocera <bnocera@redhat.com> 4.71-3
- systemd hookup and cleanups from Lennart

* Thu Sep 09 2010 Bastien Nocera <bnocera@redhat.com> 4.71-1
- Update to 4.71

* Thu Aug 26 2010 Bastien Nocera <bnocera@redhat.com> 4.70-1
- Update to 4.70

* Sat Jul 31 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 4.69-4
- Re-add Requires: dbus-bluez-pin-helper, since blueman is now in

* Sat Jul 31 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> 4.69-3
- Comment out Requires: dbus-bluez-pin-helper for bootstrapping. Otherwise
  it drags in the old blueman, built against python-2.6
* Fri Jul 23 2010 Bastien Nocera <bnocera@redhat.com> 4.69-2
- Don't allow installing bluez-compat on its own

* Fri Jul 16 2010 Bastien Nocera <bnocera@redhat.com> 4.69-1
- Update to 4.69

* Sun Jul 11 2010 Dan Horák <dan[at]danny.cz> 4.66-3
- don't require the pin helper on s390(x) now, we can disable the whole
  bluetooth stack in the future

* Mon Jun 21 2010 Bastien Nocera <bnocera@redhat.com> 4.66-2
- Move hidd, pand and dund man pages to the -compat
  sub-package (#593578)

* Mon Jun 14 2010 Bastien Nocera <bnocera@redhat.com> 4.66-1
- Update to 4.66

* Mon May 24 2010 Bastien Nocera <bnocera@redhat.com> 4.65-1
- Update to 4.65

* Thu Apr 29 2010 Bastien Nocera <bnocera@redhat.com> 4.64-1
- Update to 4.64

* Mon Apr 12 2010 Bastien Nocera <bnocera@redhat.com> 4.63-3
- And actually apply the aforementioned patch

* Mon Apr 12 2010 Bastien Nocera <bnocera@redhat.com> 4.63-2
- Fix pairing and using mice, due to recent BtIO changes

* Fri Mar 26 2010 Bastien Nocera <bnocera@redhat.com> 4.63-1
- Update to 4.63

* Mon Mar 08 2010 Bastien Nocera <bnocera@redhat.com> 4.62-1
- Update to 4.62

* Mon Feb 15 2010 Bastien Nocera <bnocera@redhat.com> 4.61-1
- Update to 4.61
- Remove Wacom tablet enabler, now in the kernel
- Fix linking with new DSO rules (#564799)

* Mon Feb 15 2010 Bastien Nocera <bnocera@redhat.com> 4.60-2
- Fix typo in init script (#558993)

* Sun Jan 10 2010 Bastien Nocera <bnocera@redhat.com> 4.60-1
- Update to 4.60

* Fri Dec 25 2009 Bastien Nocera <bnocera@redhat.com> 4.59-1
- Update to 4.59

* Mon Nov 16 2009 Bastien Nocera <bnocera@redhat.com> 4.58-1
- Update to 4.58

* Mon Nov 02 2009 Bastien Nocera <bnocera@redhat.com> 4.57-2
- Move the rfcomm.conf to the compat package, otherwise
  the comments at the top of it are confusing

* Sat Oct 31 2009 Bastien Nocera <bnocera@redhat.com> 4.57-1
- Update to 4.57

* Sat Oct 10 2009 Bastien Nocera <bnocera@redhat.com> 4.56-1
- Update to 4.56

* Fri Oct 09 2009 Bastien Nocera <bnocera@redhat.com> 4.55-2
- Update cable pairing plugin to use libudev

* Mon Oct 05 2009 Bastien Nocera <bnocera@redhat.com> 4.55-1
- Update to 4.55
- Add libcap-ng support to drop capabilities (#517660)

* Thu Sep 24 2009 Bastien Nocera <bnocera@redhat.com> 4.54-1
- Update to 4.54

* Wed Sep 16 2009 Bastien Nocera <bnocera@redhat.com> 4.53-2
- Update cable plugin for gudev changes

* Thu Sep 10 2009 Bastien Nocera <bnocera@redhat.com> 4.53-1
- Update to 4.53

* Fri Sep 04 2009 Bastien Nocera <bnocera@redhat.com> 4.52-1
- Update to 4.52

* Thu Sep 03 2009 Bastien Nocera <bnocera@redhat.com> 4.51-1
- Update to 4.51

* Tue Sep 01 2009 Bastien Nocera <bnocera@redhat.com> 4.50-2
- Remove obsoleted patches
- Add another CUPS backend patch
- Update cable pairing patch for new build system

* Tue Sep 01 2009 Bastien Nocera <bnocera@redhat.com> 4.50-1
- Update to 4.50

* Tue Aug 25 2009 Karsten Hopp <karsten@redhat.com> 4.47-6
- don't buildrequire libusb1 on s390*

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 4.47-5
- More upstream CUPS fixes

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 4.47-4
- Fix cups discovery the first time we discover a device

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.47-3
- Use bzipped upstream tarball.

* Wed Aug 05 2009 Bastien Nocera <bnocera@redhat.com> 4.47-2
- Remove hid2hci calls, they're in udev now
- Work-around udev bug, bluetoothd wasn't getting enabled
  on coldplug

* Sun Aug 02 2009 Bastien Nocera <bnocera@redhat.com> 4.47-1
- Update to 4.47

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 4.46-3
- Add rfkill plugin to restore the state of the adapters
  after coming back from a blocked adapter

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Bastien Nocera <bnocera@redhat.com> 4.46-1
- Update to 4.46

* Wed Jul 08 2009 Bastien Nocera <bnocera@redhat.com> 4.45-1
- Update to 4.45

* Tue Jul 07 2009 Bastien Nocera <bnocera@redhat.com> 4.44-1
- Update to 4.44

* Fri Jul 03 2009 Bastien Nocera <bnocera@redhat.com> 4.43-2
- Up the required udev requires so bluetoothd gets started
  on boot when an adapter is present

* Fri Jul 03 2009 Bastien Nocera <bnocera@redhat.com> 4.43-1
- Update to 4.43

* Sun Jun 21 2009 Bastien Nocera <bnocera@redhat.com> 4.42-2
- Update to 4.42

* Thu Jun 11 2009 Bastien Nocera <bnocera@redhat.com> 4.41-2
- Switch to on-demand start/stop using udev

* Mon Jun 08 2009 Bastien Nocera <bnocera@redhat.com> 4.41-1
- Update to 4.41

* Fri Jun 05 2009 Bastien Nocera <bnocera@redhat.com> 4.40-2
- Add patch to allow Sixaxis pairing

* Tue May 19 2009 Bastien Nocera <bnocera@redhat.com> 4.40-1
- Update to 4.40

* Sat May 09 2009 Bastien Nocera <bnocera@redhat.com> 4.39-1
- Update to 4.39

* Tue May 05 2009 Petr Lautrbach <plautrba@redhat.com> 4.38-3
- Start/stop the bluetooth service via udev (#484345)

* Tue May 05 2009 Bastien Nocera <bnocera@redhat.com> 4.38-2
- Add patch to activate the Socket Mobile CF kit (#498756)

* Mon May 04 2009 Bastien Nocera <bnocera@redhat.com> 4.38-1
- Update to 4.38

* Wed Apr 29 2009 Bastien Nocera <bnocera@redhat.com> 4.37-2
- Split off dund, pand, hidd, and rfcomm helper into a compat package
  (#477890, #473892)

* Thu Apr 23 2009 - Bastien Nocera <bnocera@redhat.com> - 4.37-1
- Update to 4.37

* Fri Apr 17 2009 - Bastien Nocera <bnocera@redhat.com> - 4.36-1
- Update to 4.36

* Sat Apr 11 2009 - Bastien Nocera <bnocera@redhat.com> - 4.35-1
- Update to 4.35

* Fri Apr 03 2009 - Bastien Nocera <bnocera@redhat.com> - 4.34-3
- Avoid disconnecting audio devices straight after they're connected

* Fri Apr 03 2009 - Bastien Nocera <bnocera@redhat.com> - 4.34-2
- Don't crash when audio devices are registered and the adapter
  is removed

* Sun Mar 29 2009 - Bastien Nocera <bnocera@redhat.com> - 4.34-1
- Update to 4.34

* Tue Mar 24 2009 - Bastien Nocera <bnocera@redhat.com> - 4.33-11
- Fix a possible crasher

* Mon Mar 16 2009 - Bastien Nocera <bnocera@redhat.com> - 4.33-1
- Update to 4.33

* Sat Mar 14 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-10
- Fix a couple of warnings in the CUPS/BlueZ 4.x patch

* Fri Mar 13 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-9
- Switch Wacom Bluetooth tablet to mode 2

* Mon Mar 09 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-8
- Port CUPS backend to BlueZ 4.x

* Mon Mar 09 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-7
- A (slightly) different fix for parsing to XML when it contains a NULL

* Mon Mar 09 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-6
- Fix sdp_copy_record(), so records are properly exported through D-Bus

* Fri Mar 06 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-5
- Fix SDP parsing to XML when it contains NULLs

* Thu Mar 05 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-4
- Work-around broken devices that export their names in ISO-8859-1
  (#450081)

* Thu Mar 05 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-3
- Fix permissions on the udev rules (#479348)

* Wed Mar 04 2009 - Bastien Nocera <bnocera@redhat.com> - 4.32-2
- Own /usr/lib*/bluetooth and children (#474632)

* Mon Mar 2 2009 Lennart Poettering <lpoetter@redhat.com> - 4.32-1
- Update to 4.32

* Thu Feb 26 2009 Lennart Poettering <lpoetter@redhat.com> - 4.31-1
- Update to 4.31

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 - Bastien Nocera <bnocera@redhat.com> - 4.30-2
- Fix the cups backend being a libtool stub

* Thu Feb 12 2009 - Bastien Nocera <bnocera@redhat.com> - 4.30-1
- Update to 4.30

* Thu Feb 12 2009 Karsten Hopp <karsten@redhat.com> 4.29-3
- disable 0001-Add-icon-for-other-audio-device.patch, already upstream

* Thu Feb 12 2009 Karsten Hopp <karsten@redhat.com> 4.29-2
- bluez builds fine on s390(x) and the packages are required to build
  other packages, drop ExcludeArch

* Mon Feb 09 2009 - Bastien Nocera <bnocera@redhat.com> - 4.29-1
- Update to 4.29

* Mon Feb 02 2009 - Bastien Nocera <bnocera@redhat.com> - 4.28-1
- Update to 4.28

* Mon Jan 19 2009 - Bastien Nocera <bnocera@redhat.com> - 4.27-1
- Update to 4.27

* Fri Jan 09 2009 - Bastien Nocera <bnocera@redhat.com> - 4.26-1
- Update to 4.26

* Sat Jan 03 2009 - Bastien Nocera <bnocera@redhat.com> - 4.25-1
- Update to 4.25

* Tue Dec 09 2008 - Bastien Nocera <bnocera@redhat.com> - 4.22-2
- Fix D-Bus configuration for latest D-Bus (#475069)

* Mon Dec 08 2008 - Bastien Nocera <bnocera@redhat.com> - 4.22-1
- Update to 4.22

* Mon Dec 01 2008 - Bastien Nocera <bnocera@redhat.com> - 4.21-1
- Update to 4.21

* Fri Nov 21 2008 - Bastien Nocera <bnocera@redhat.com> - 4.19-1
- Update to 4.19

* Mon Nov 17 2008 - Bastien Nocera <bnocera@redhat.com> - 4.18-1
- Update to 4.18

* Mon Oct 27 2008 - Bastien Nocera <bnocera@redhat.com> - 4.17-2
- Own /var/lib/bluetooth (#468717)

* Sun Oct 26 2008 - Bastien Nocera <bnocera@redhat.com> - 4.17-1
- Update to 4.17

* Tue Oct 21 2008 - Bastien Nocera <bnocera@redhat.com> - 4.16-1
- Update to 4.16

* Mon Oct 20 2008 - Bastien Nocera <bnocera@redhat.com> - 4.15-1
- Update to 4.15

* Fri Oct 17 2008 - Bastien Nocera <bnocera@redhat.com> - 4.14-2
- Add script to autoload uinput on startup, so the PS3 remote
  works out-of-the-box

* Fri Oct 17 2008 - Bastien Nocera <bnocera@redhat.com> - 4.14-1
- Update to 4.14

* Tue Oct 14 2008 - Bastien Nocera <bnocera@redhat.com> - 4.13-3
- Update udev rules (#246840)

* Mon Oct 13 2008 - Bastien Nocera <bnocera@redhat.com> - 4.13-2
- Fix PS3 BD remote input event generation

* Fri Oct 10 2008 - Bastien Nocera <bnocera@redhat.com> - 4.13-1
- Update to 4.13

* Mon Oct 06 2008 - Bastien Nocera <bnocera@redhat.com> - 4.12-1
- Update to 4.12

* Sat Oct 04 2008 - Bastien Nocera <bnocera@redhat.com> - 4.11-1
- Update to 4.11

* Fri Oct 03 2008 - Bastien Nocera <bnocera@redhat.com> - 4.10-1
- Update to 4.10

* Mon Sep 29 2008 - Bastien Nocera <bnocera@redhat.com> - 4.9-1
- Update to 4.9

* Mon Sep 29 2008 - Bastien Nocera <bnocera@redhat.com> - 4.8-1
- Update to 4.8

* Fri Sep 26 2008 - Bastien Nocera <bnocera@redhat.com> - 4.7-1
- Update to 4.7

* Wed Sep 24 2008 - Bastien Nocera <bnocera@redhat.com> - 4.6-4
- Fix patch application

* Wed Sep 24 2008 - Bastien Nocera <bnocera@redhat.com> - 4.6-3
- Add fuzz

* Wed Sep 24 2008 - Bastien Nocera <bnocera@redhat.com> - 4.6-2
- Fix possible crasher on resume from suspend

* Sun Sep 14 2008 - David Woodhouse <David.Woodhouse@intel.com> - 4.6-1
- Update to 4.6

* Fri Sep 12 2008 - David Woodhouse <David.Woodhouse@intel.com> - 4.5-4
- SDP browse fixes

* Fri Sep 12 2008 - David Woodhouse <David.Woodhouse@intel.com> - 4.5-3
- Bluez-alsa needs to provide/obsolete bluez-utils-alsa
- Use versioned Obsoletes:

* Fri Sep 12 2008 - David Woodhouse <David.Woodhouse@intel.com> - 4.5-2
- Change main utils package name to 'bluez'; likewise its subpackages
- Remove references to obsolete initscripts (hidd,pand,dund)

* Fri Sep 12 2008 - Bastien Nocera <bnocera@redhat.com> - 4.5-1
- Update to 4.5
- Fix initscript to actually start bluetoothd by hand
- Add chkconfig information to the initscript

* Tue Sep 09 2008 - David Woodhouse <David.Woodhouse@intel.com> - 4.4-2
- Fix rpmlint problems
- Fix input device handling

* Tue Sep 09 2008 - Bastien Nocera <bnocera@redhat.com> - 4.4-1
- Update to 4.4
- Update source address, and remove unneeded deps (thanks Marcel)

* Mon Aug 11 2008 - Bastien Nocera <bnocera@redhat.com> - 4.1-1
- Initial build
