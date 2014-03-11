
# Building the extra print profiles requires colprof, +4Gb of RAM and
# quite a lot of time. Don't enable this for test builds.
%define enable_print_profiles 0

# SANE is pretty insane when it comes to handling devices, and we get AVCs
# popping up all over the place.
%define enable_sane 0

# Don't build the print profiles for secondary architectures on the
# logic that these are probably not doing press proofing or editing
# in different CMYK spaces
%ifarch %{ix86} x86_64
%define build_print_profiles %{?enable_print_profiles}
%else
%define build_print_profiles 0
%endif

Summary:   Color daemon
Name:      colord
Version:   0.1.33
Release:   1%{?dist}
License:   GPLv2+ and LGPLv2+
URL:       http://www.freedesktop.org/software/colord/
Source0:   http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz

BuildRequires: dbus-devel
BuildRequires: docbook-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: intltool
BuildRequires: systemd-devel
BuildRequires: lcms2-devel >= 2.2
BuildRequires: libgudev1-devel
BuildRequires: polkit-devel >= 0.103
BuildRequires: sqlite-devel
BuildRequires: gobject-introspection-devel
BuildRequires: vala-tools
BuildRequires: libgusb-devel
BuildRequires: gtk-doc
BuildRequires: color-filesystem
%if 0%{?build_print_profiles}
BuildRequires: argyllcms
%endif

# for SANE support
%if 0%{?enable_sane}
BuildRequires: sane-backends-devel
BuildRequires: dbus-devel
%endif

Requires: color-filesystem
Requires: systemd-units
Requires(pre): shadow-utils

# Self-obsoletes to fix the multilib upgrade path
Obsoletes: colord < 0.1.27-3

# obsolete separate profiles package
Obsoletes: shared-color-profiles <= 0.1.6-2
Provides: shared-color-profiles

%description
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package libs
Summary: Color daemon library

%description libs
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package devel
Summary: Development package for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Obsoletes: colorhug-client-devel <= 0.1.13

%description devel
Files for development with %{name}.

%package devel-docs
Summary: Developer documentation package for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
Documentation for development with %{name}.

%package extra-profiles
Summary: More color profiles for color management that are less commonly used
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

# obsolete separate profiles package
Obsoletes: shared-color-profiles-extra <= 0.1.6-2
Provides: shared-color-profiles-extra

%description extra-profiles
More color profiles for color management that are less commonly used.
This may be useful for CMYK soft-proofing or for extra device support.

%prep
%setup -q

%build
# we can't use _hardened_build here, see
# https://bugzilla.redhat.com/show_bug.cgi?id=892837
export CFLAGS='-fPIC %optflags'
export LDFLAGS='-pie -Wl,-z,now -Wl,-z,relro'

# Set ~2 GiB limit so that colprof is forced to work in chunks when
# generating the print profile rather than trying to allocate a 3.1 GiB
# chunk of RAM to put the entire B-to-A tables in.
ulimit -Sv 2000000
%configure \
        --with-daemon-user=colord \
        --enable-gtk-doc \
        --enable-vala \
%if 0%{?build_print_profiles}
        --enable-print-profiles \
%else
        --disable-print-profiles \
%endif
%if 0%{?enable_sane}
        --enable-sane \
%endif
        --disable-static \
        --disable-rpath \
        --disable-examples \
        --disable-silent-rules \
        --disable-dependency-tracking

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove static libs and libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# databases
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/mapping.db
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/colord/storage.db

%find_lang %{name}

%pre
getent group colord >/dev/null || groupadd -r colord
getent passwd colord >/dev/null || \
    useradd -r -g colord -d /var/lib/colord -s /sbin/nologin \
    -c "User for colord" colord
exit 0

%post
/sbin/ldconfig
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%postun
/sbin/ldconfig
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc README AUTHORS NEWS COPYING
%{_libexecdir}/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord
%attr(755,colord,colord) %dir %{_localstatedir}/lib/colord/icc
%{_bindir}/*
%{_datadir}/glib-2.0/schemas/org.freedesktop.ColorHelper.gschema.xml
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ColorManager.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.color.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ColorManager.service
%{_datadir}/man/man1/*.1.gz
%{_datadir}/colord
%config %{_sysconfdir}/colord.conf
/usr/lib/udev/rules.d/*.rules
%{_libdir}/colord-sensors
%{_libdir}/colord-plugins
%verify(not size md5 mtime) %attr(-,colord,colord) %{_localstatedir}/lib/colord/*.db
/usr/lib/systemd/system/colord.service
%{_sysconfdir}/bash_completion.d/*-completion.bash

# session helper
%{_libexecdir}/colord-session
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorHelper.xml
%{_datadir}/dbus-1/services/org.freedesktop.ColorHelper.service

# sane helper
%if 0%{?enable_sane}
%{_libexecdir}/colord-sane
%endif

# common colorspaces
%dir %{_icccolordir}/colord
%{_icccolordir}/colord/AdobeRGB1998.icc
%{_icccolordir}/colord/ProPhotoRGB.icc
%{_icccolordir}/colord/SMPTE-C-RGB.icc
%{_icccolordir}/colord/sRGB.icc

# so we can display at least something in the default dropdown
%if 0%{?build_print_profiles}
%{_icccolordir}/colord/FOGRA39L_coated.icc
%endif

# monitor test profiles
%{_icccolordir}/colord/Bluish.icc

# named color profiles
%{_icccolordir}/colord/x11-colors.icc

%files libs
%doc COPYING
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/*.typelib

%files extra-profiles
%if 0%{?build_print_profiles}
%{_icccolordir}/colord/FOGRA27L_coated.icc
%{_icccolordir}/colord/FOGRA28L_webcoated.icc
%{_icccolordir}/colord/FOGRA29L_uncoated.icc
%{_icccolordir}/colord/FOGRA30L_uncoated_yellowish.icc
%{_icccolordir}/colord/FOGRA40L_SC_paper.icc
%{_icccolordir}/colord/FOGRA45L_lwc.icc
%{_icccolordir}/colord/FOGRA47L_uncoated.icc
%{_icccolordir}/colord/GRACoL*.icc
%{_icccolordir}/colord/IFRA26S_2004_newsprint.icc
%{_icccolordir}/colord/SNAP*.icc
%{_icccolordir}/colord/SWOP*.icc
%endif

# other colorspaces not often used
%{_icccolordir}/colord/AppleRGB.icc
%{_icccolordir}/colord/BestRGB.icc
%{_icccolordir}/colord/BetaRGB.icc
%{_icccolordir}/colord/BruceRGB.icc
%{_icccolordir}/colord/CIE-RGB.icc
%{_icccolordir}/colord/ColorMatchRGB.icc
%{_icccolordir}/colord/DonRGB4.icc
%{_icccolordir}/colord/ECI-RGBv1.icc
%{_icccolordir}/colord/ECI-RGBv2.icc
%{_icccolordir}/colord/EktaSpacePS5.icc
%{_icccolordir}/colord/Gamma*.icc
%{_icccolordir}/colord/NTSC-RGB.icc
%{_icccolordir}/colord/PAL-RGB.icc
%{_icccolordir}/colord/SwappedRedAndGreen.icc
%{_icccolordir}/colord/WideGamutRGB.icc

# other named color profiles not generally useful
%{_icccolordir}/colord/Crayons.icc

%files devel
%{_includedir}/colord-1
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/colord.vapi

%files devel-docs
%dir %{_datadir}/gtk-doc/html/colord
%{_datadir}/gtk-doc/html/colord/*

%changelog
* Tue Apr 16 2013 Richard Hughes <richard@hughsie.com> 0.1.33-1
- New upstream version
- Add some translated profile descriptions for the CMYK profiles
- Add the FOGRA45L and FOGRA47L CMYK and eciRGBv1 profiles
- Check the generated CCMX matrix for invalid data
- Do not print a warning if the DBus property does not exist
- Ensure mbstowcs() has an LC_CTYPE of 'en_US.UTF-8'
- Always write C-locale floating point values in IT8 files
- Initialize the value of the CCMX matrix
- Never promote localized v2 ICC profiles to v4
- Rename ISOnewspaper26 to IFRA26S_2004_newsprint

* Thu Mar 28 2013 Richard Hughes <richard@hughsie.com> 0.1.32-1
- New upstream version
- Add a new tool 'cd-iccdump' that can dump V4 and V2 profiles
- Add translated descriptions to the ICC profiles

* Mon Mar 18 2013 Richard Hughes <richard@hughsie.com> 0.1.31-1
- New upstream version
- Calculate the display calibration based on the Lab and target display gamma
- Interpolate the gamma data to the VCGT size using Akima
- Add some more display vendor names to the display fixup table
- Fix the argyll sensor driver when using the ColorMunki Smile
- Fix the gamut warning to check primaries wider than CIERGB and ProPhoto
- Move the private sensor libraries out of the pure lib space

* Mon Feb 18 2013 Richard Hughes <richard@hughsie.com> 0.1.30-1
- New upstream version
- Append -private to the driver libraries as they have no headers installed
- Do not show duplicate profiles when icc-profiles-openicc is installed
- Speed up the daemon loading and use less I/O at startup

* Mon Feb 04 2013 Richard Hughes <richard@hughsie.com> 0.1.29-1
- New upstream version
- Add a --verbose and --version argument to colormgr
- Add DTP94 native sensor support
- Allow profiles to have a 'score' which affects the standard space
- Change the Adobe RGB description to be 'Compatible with Adobe RGB (1998)'
- Detect profiles from adobe.com and color.org and add metadata
- Do not auto-add profiles due to device-id metadata if they have been removed
- Ensure profiles with MAPPING_device_id get auto-added to devices
- Install various helper libraries for access to hardware
- Set the additional 'OwnerCmdline' metadata on each device

* Fri Jan 18 2013 Richard Hughes <richard@hughsie.com> 0.1.28-2
- Backport some fixes from upstream for gnome-settings-daemon.

* Wed Jan 16 2013 Richard Hughes <richard@hughsie.com> 0.1.28-1
- New upstream version
- Add some default GSetting schema values for the calibration helper
- Add the sensor images as metadata on the D-Bus interface
- Quit the session helper if the device or sensor was not found

* Mon Jan 14 2013 Richard Hughes <richard@hughsie.com> 0.1.27-4
- Add BR systemd-devel so the seat tracking stuff works
- Build with full compiler output
- Do not build the profiles in parallel, backported from upstream
- Limit the memory allocation to 2GiB when building profiles
- Do not attempt to build the print profiles on ARM or PPC hardware

* Fri Jan 11 2013 Kalev Lember <kalevlember@gmail.com> 0.1.27-3
- Added self-obsoletes to 'colord' subpackage to fix the multilib upgrade path

* Thu Jan 10 2013 Kalev Lember <kalevlember@gmail.com> 0.1.27-2
- Split out libcolord to colord-libs subpackage, so that the daemon package
  doesn't get multilibbed

* Tue Jan 08 2013 Richard Hughes <richard@hughsie.com> 0.1.27-1
- New upstream version
- Add some more calibration attach images
- Import shared-color-profiles into colord
- Install a header with all the session helper defines

* Mon Jan  7 2013 Matthias Clasen <mclasen@redhat.com> 0.1.26-2
- Enable hardened build

* Wed Dec 19 2012 Richard Hughes <richard@hughsie.com> 0.1.26-1
- New upstream version
- Add a session helper that can be used to calibrate the screen
- Add some defines for the Spyder4 display colorimeter
- Add support for reading and writing .cal files to CdIt8
- Add the ability to 'disable' a device from a color POV
- Create ICCv2 profiles when using cd-create-profile
- Use enumerated error values in the client library
- Use spotread when there is no native sensor driver

* Mon Nov 26 2012 Richard Hughes <richard@hughsie.com> 0.1.25-1
- New upstream version
- Add a create-standard-space sub-command to cd-create-profile
- Add a profile metadata key of 'License'
- Add a set-version command to the cd-fix-profile command line tool
- Create linear vcgt tables when using create-x11-gamma
- Fix GetStandardSpace so it can actually work
- Move the named color examples to shared-color-profiles

* Wed Nov 21 2012 Richard Hughes <richard@hughsie.com> 0.1.24-2
- Apply a patch from upstream so we can use cd-fix-profile in
  situations without D-Bus.

* Fri Oct 26 2012 Richard Hughes <richard@hughsie.com> 0.1.24-1
- New upstream version
- Fix a critical warning when user tries to dump a non-icc file
- Remove libsane support and rely only on udev for scanner information
- Set the seat for devices created in the session and from udev

* Wed Aug 29 2012 Richard Hughes <richard@hughsie.com> 0.1.23-1
- New upstream version
- Assorted documentation fixes
- Do not try to add duplicate sysfs devices

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Richard Hughes <richard@hughsie.com> 0.1.22-1
- New upstream version
- Split out colord-gtk to a new sub-project to prevent a dep loop
- Add many generic introspection type arguments
- Check any files in /usr/share/color/icc have the content type
- Do not create the same object paths if two sensors are plugged in
- Fix the udev rules entry for the i1Display3

* Tue May 22 2012 Richard Hughes <richard@hughsie.com> 0.1.21-1
- New upstream version
- Do not install any parts of colord-sane if --disable-sane is specified
- Fix InstallSystemWide() by not writing a private file
- Save the CCMX and ITx files to be compatible with argyllcms
- The ColorHug has a new VID and PID

* Wed May 09 2012 Richard Hughes <richard@hughsie.com> 0.1.20-1
- New upstream version
- Add a sensor-set-options command to the colormgr tool
- Add the concept of 'options' on each color sensor device
- Enable gtk-doc in the default distro build

* Tue Apr 17 2012 Richard Hughes <richard@hughsie.com> 0.1.19-1
- New upstream version
- Add a user suffix to the object path of user-created devices and profiles

* Thu Mar 29 2012 Richard Hughes <richard@hughsie.com> 0.1.18-2
- Disable PrivateNetwork=1 as it breaks sensor hotplug.

* Thu Mar 15 2012 Richard Hughes <richard@hughsie.com> 0.1.18-1
- New upstream version
- Add a Manager.CreateProfileWithFd() method for QtDBus
- Split out the SANE support into it's own process
- Fix a small leak when creating devices and profiles in clients
- Fix cd-fix-profile to add and remove metadata entries
- Install per-machine profiles in /var/lib/colord/icc

* Wed Feb 22 2012 Richard Hughes <richard@hughsie.com> 0.1.17-1
- New upstream version
- Add an LED sample type
- Add PrivateNetwork and PrivateTmp to the systemd service file
- Fix InstallSystemWide() when running as the colord user

* Fri Jan 20 2012 Matthias Clasen <mclasen@redha.com> - 0.1.16-4
- Fix some obvious bugs

* Tue Jan 17 2012 Richard Hughes <richard@hughsie.com> 0.1.16-1
- New upstream version
- Now runs as a colord user rather than as root.
- Support more ICC metadata keys
- Install a systemd service file
- Support 2nd generation Huey hardware

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Richard Hughes <richard@hughsie.com> 0.1.15-1
- New upstream version
- This release fixes an important security bug: CVE-2011-4349.
- Do not crash the daemon if adding the device to the db failed
- Fix a memory leak when getting properties from a device

* Tue Nov 01 2011 Richard Hughes <richard@hughsie.com> 0.1.14-1
- New upstream version
- Remove upstreamed patches

* Mon Oct 03 2011 Richard Hughes <richard@hughsie.com> 0.1.13-1
- New upstream version
- Ensure uid 0 can always create devices and profiles
- Reduce the CPU load of clients when assigning profiles

* Tue Aug 30 2011 Richard Hughes <richard@hughsie.com> 0.1.12-1
- New upstream version

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> 0.1.11-2
- Remove the sedding libtool's internals as it breaks
  generation of the GObject Introspection data.

* Mon Aug 01 2011 Richard Hughes <richard@hughsie.com> 0.1.11-1
- New upstream version

* Wed Jul 06 2011 Richard Hughes <richard@hughsie.com> 0.1.10-1
- New upstream version

* Mon Jun 13 2011 Richard Hughes <richard@hughsie.com> 0.1.9-1
- New upstream version

* Thu Jun 02 2011 Richard Hughes <richard@hughsie.com> 0.1.8-1
- New upstream version
- Add a webcam device kind
- Add a timestamp when making profiles default
- Add support for reading and writing ICC profile metadata
- Allow the client to pass file descriptors out of band to CreateProfile
- Prettify the device vendor and model names
- Split out the sensors into runtime-loadable shared objects
- Provide some GIO async variants for the methods in CdClient
- Ensure GPhoto2 devices get added to the device list

* Fri May 06 2011 Richard Hughes <richard@hughsie.com> 0.1.7-1
- New upstream version.
- Create /var/lib/colord at buildtime not runtime for SELinux
- Ensure profiles with embedded profile checksums are parsed correctly
- Move the colorimeter rules to be run before 70-acl.rules
- Stop watching the client when the sensor is finalized
- Ensure the source is destroyed when we unref CdUsb to prevent a crash
- Only enable the volume mount tracking when searching volumes

* Tue Apr 26 2011 Richard Hughes <rhughes@redhat.com> 0.1.6-2
- Own /var/lib/colord and /var/lib/colord/*.db

* Sun Apr 24 2011 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream version.

* Thu Mar 31 2011 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream version.

* Wed Mar 09 2011 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream version.

* Mon Feb 28 2011 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Richard Hughes <richard@hughsie.com> 0.1.1-2
- Rebuild in the vain hope koji isn't broken today.

* Wed Jan 26 2011 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream version.

* Thu Jan 13 2011 Richard Hughes <richard@hughsie.com> 0.1.0-1
- Initial version for Fedora package review.
