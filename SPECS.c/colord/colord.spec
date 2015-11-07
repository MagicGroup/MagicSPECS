
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
 %if !0%{?rhel}
  %define build_print_profiles %{?enable_print_profiles}
 %endif
%endif

Summary:   Color daemon
Name:      colord
Version:	1.2.12
Release:   2%{?dist}
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
%if !0%{?rhel}
BuildRequires: bash-completion
%endif
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
Requires: colord-libs%{?_isa} = %{version}-%{release}

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
%if 0%{?rhel}
        --disable-bash-completion \
%endif
%if !0%{?rhel}
        --enable-libcolordcompat \
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

%check
# known failure as of 1.1.5: colorhug/device-queue
make check || \
{ rc=$?; find . -name test-suite.log | xargs cat; } # exit $rc; }

%pre
getent group colord >/dev/null || groupadd -r colord
getent passwd colord >/dev/null || \
    useradd -r -g colord -d /var/lib/colord -s /sbin/nologin \
    -c "User for colord" colord
exit 0

%post
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%systemd_post colord.service

%preun
%systemd_preun colord.service

%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%systemd_postun colord.service

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.md AUTHORS NEWS COPYING
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
%if !0%{?rhel}
%{_datadir}/bash-completion/completions/colormgr
%endif
/usr/lib/udev/rules.d/*.rules
%{_libdir}/colord-sensors
%{_libdir}/colord-plugins
%ghost %attr(-,colord,colord) %{_localstatedir}/lib/colord/*.db
/usr/lib/systemd/system/colord.service

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
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.2.12-2
- 更新到 1.2.12

* Fri Feb 28 2014 Richard Hughes <richard@hughsie.com> 1.1.7-1
- New upstream version
- Use the new cmsContext functionality in LCMS 2.6
- Fix the GObject introspection for cd_device_get_profiles()
- Load the profile defaults when using cd_icc_create_default()

* Fri Feb 28 2014 Rex Dieter <rdieter@fedoraproject.org> 1.1.6-3
- revert Conflicts: icc-profiles-openicc pending (hopefully) better solution (#1069672)

* Tue Jan 21 2014 Richard Hughes <richard@hughsie.com> 1.1.6-2
- We don't actually need the valgrind BR...

* Tue Jan 21 2014 Dan Horák <dan[at]danny.cz> - 1.1.6-1.1
- valgrind is available only on selected arches

* Mon Jan 20 2014 Richard Hughes <richard@hughsie.com> 1.1.6-1
- New upstream version
- Fix the tag 'size' when viewing a profile in cd-iccdump
- Only include libudev in Requires.private on Linux
- Use the corect sensor-kind values for GretagMacbeth sensors
- Do not use G_GNUC_WARN_UNUSED_RESULT when uninhibiting
- Handle failure to initialise GUsb in self-tests

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.1.5-3
- Move ldconfig %%post* scriptlets to -libs.
- Run test suite during build.
- Fix bogus date in %%changelog.

* Wed Dec 11 2013 Richard Hughes <richard@hughsie.com> 1.1.5-2
- Add conflict on icc-profiles-openicc
- The OpenICC profiles are not really compatible for a few reasons:
 * The profiles are duplicates of the ones shipped in the colord package
 * The don't contain the correct metadata so the standard spaces show up in the
   device profile chooser.
 * The profiles don't contain an embedded ID, so colord has to hash them all
   manually at startup, which makes colord look bad in bootchart
 * A duplicate mime rule is installed which matches shared-mime-info one

* Wed Dec 11 2013 Richard Hughes <richard@hughsie.com> 1.1.5-1
- New upstream version
- Do not crash when moving the sensor position during calibration
- Do not crash with zero-sized ICC file
- Do not create legacy locations
- Ensure the ICC version is set when creating from the EDID
- Ensure the parsed EDID strings are valid UTF-8
- Fix crash when using cd_color_get_blackbody_rgb()
- Never add USB hubs as scanner devices even if tagged
- Never create color managed webcam devices

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> 1.1.4-1
- New upstream version
- Only syslog() profile additions when they're added via DBus
- Reset the LCMS log handlers to default after use
- Use the threadsafe versions of the LCMS functions
- Resolves: #1016425

* Wed Oct 30 2013 Richard Hughes <richard@hughsie.com> 1.1.3-1
- New upstream version
- Never print incomplete 'colormgr dump' output
- Restrict the length of key and values when setting metadata

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> 1.1.2-1
- New upstream version
- Add a 'dump' colormgr command to aid debugging
- Allow profiles to be added or removed when the device is not enabled
- Always return soft-add calibration profiles before soft-add EDID profiles
- Do not mix up device paths and device IDs in the documentation
- Fix an error when building the print profiles
- Fix the AdobeRGB and WideGamutRGB gamma values
- Fix up various vendor quirks
- Migrate from usb_id and usb_db to udev builtins usb_id and hwdb
- Set 'GAMUT_coverage(srgb)' when generating standard space profiles
- Show a warning for incorrect or extra command line arguments
- Use %ghost to avoid removing databases on upgrades
- Use the exact D50 whitepoint values

* Tue Jul 30 2013 Richard Hughes <richard@hughsie.com> 1.1.1-1
- New upstream version
- This release bumps the soname of libcolord as long deprecated methods have
  finally been removed. Any programs that link against libcolord will have to
  be recompiled against this new version.
- This unstable branch is full of new features and experimental code, and
  therefore this release will be restricted to rawhide.
- Remove the now-unused /etc/colord.conf
- Update the colormgr man page to reflect reality

* Thu Jul 18 2013 Matthias Clasen <mclasen@redhat.com> 1.0.2-2
- Add an archful dep to silence rpmdiff

* Sun Jul 07 2013 Richard Hughes <richard@hughsie.com> 1.0.2-1
- New upstream version
- Add cd_icc_save_data() so that we can easily set _ICC_PROFILE
- Add CdIccStore to monitor directories of ICC profiles
- Add SystemVendor and SystemModel properties to the main interface
- Allow to specify a non-qualified path when using FindProfileByFilename
- Allow using the key 'Filename' when using FindProfileByProperty
- Always return the error if any sync method failed
- Fix GObject introspection when getting lists
- Fix GObject introspection when getting metadata

* Tue Jun 11 2013 Richard Hughes <richard@hughsie.com> 1.0.1-1
- New upstream version
- Do not unconditionally enable BPC on the color transform
- Fix profile created time for non-UTC timezones
- Record the gamma table in the session helper error message

* Mon May 13 2013 Richard Hughes <richard@hughsie.com> 1.0.0-1
- New upstream version
- Add a config option for monitors with identical EDID values
- Allow a different input and output format in CdTransform
- Build all installed binaries with PIE
- Build the colord binary with full RELRO
- Do not show a warning when using 'colormgr device-get-profile-for-qualifier'
- Fix crash in cd-iccdump by working around an lcms2 bug
- Fix using the color sensors on ARM hardware
- Set the STANDARD_space metadata for the print profiles
- Show all the translations when dumping an ICC profile

* Wed May 01 2013 Richard Hughes <richard@hughsie.com> 0.1.34-1
- New upstream version
- Add a ICC transform object for simple RGB conversions
- Add a warning for RGB profiles with unlikely whitepoint values
- Add Qt DBus annotations
- Allow clients to call org.freedesktop.DBus.Peer
- Correct a lot more company names when creating devices
- Do not automatically add EDID profiles with warnings to devices
- Increase the delay between patches in the session-helper
- Install the bash completion support into /usr

* Wed Apr 24 2013 Václav Pavlín <vpavlin@redhat.com> - 0.1.33-2
- Add new systemd macros (#856659)

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
