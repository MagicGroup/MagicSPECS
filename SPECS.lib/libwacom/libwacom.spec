%global udevdir %(pkg-config --variable=udevdir udev)

Name:           libwacom

Version:        0.7.1
Release:        1%{?dist}
Summary:        Tablet Information Client Library
Requires:       %{name}-data

Group:          System Environment/Libraries
License:        MIT
URL:            http://linuxwacom.sourceforge.net

Source0:        http://prdownloads.sourceforge.net/linuxwacom/%{name}/%{name}-%{version}.tar.bz2
Source1:        libwacom.rules

BuildRequires:  autoconf automake libtool doxygen
BuildRequires:  glib2-devel libgudev1-devel
BuildRequires:  systemd-devel

%description
%{name} is a library that provides information about Wacom tablets and
tools. This information can then be used by drivers or applications to tweak
the UI or general settings to match the physical tablet.

%package devel
Summary:        Tablet Information Client Library Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Tablet information client library library development package.

%package data
Summary:        Tablet Information Client Library Library Data Files
BuildArch:      noarch

%description data
Tablet information client library library data files.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d ${RPM_BUILD_ROOT}/%{udevdir}/rules.d
install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}/%{udevdir}/rules.d/65-libwacom.rules

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README 
%{_libdir}/libwacom.so.*
%{udevdir}/rules.d/65-libwacom.rules
%{_bindir}/libwacom-list-local-devices

%files devel
%doc COPYING
%dir %{_includedir}/libwacom-1.0/
%dir %{_includedir}/libwacom-1.0/libwacom
%{_includedir}/libwacom-1.0/libwacom/libwacom.h
%{_libdir}/libwacom.so
%{_libdir}/pkgconfig/libwacom.pc

%files data
%doc COPYING
%dir %{_datadir}/libwacom
%{_datadir}/libwacom/*.tablet
%{_datadir}/libwacom/*.stylus
%dir %{_datadir}/libwacom/layouts
%{_datadir}/libwacom/layouts/*.svg

%changelog
* Tue Apr 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-1
- libwacom 0.7.1

* Fri Feb 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7-3
- Install into correct udev rules directory (#913723)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.7-1
- libwacom 0.7

* Fri Nov 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6.1-1
- libwacom 0.6.1
- update udev.rules files for new tablet descriptions

* Fri Aug 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-5
- remove %defattr, not necessary anymore

* Mon Jul 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-4
- ... and install the rules in %libdir

* Mon Jul 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-3
- udev rules can go into %libdir now

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-1
- libwacom 0.6

* Tue May 08 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-3
- Fix crash with WACf* serial devices (if not inputattach'd) (#819191)

* Thu May 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-2
- Fix gnome-control-center crash for Bamboo Pen & Touch
- Generic styli needs to have erasers, default to two tools.

* Wed May 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-1
- Update to 0.5
- Fix sources again - as long as Source0 points to sourceforge this is a bz2

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Update to 0.4

* Thu Mar 22 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-6
- Fix udev rules generator patch to apply ENV{ID_INPUT_TOUCHPAD} correctly
  (#803314)

* Thu Mar 08 2012 Olivier Fourdan <ofourdan@redhat.com> 0.3-5
- Mark data subpackage as noarch and make it a requirement for libwacom
- Use generated udev rule file to list only known devices from libwacom
  database

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-4
- libwacom-0.3-add-list-devices.patch: add API to list devices
- libwacom-0.3-add-udev-generator.patch: add a udev rules generater tool
- libwacom-0.3-add-bamboo-one.patch: add Bamboo One definition

* Tue Feb 21 2012 Olivier Fourdan <ofourdan@redhat.com> - 0.3-2
- Add udev rules to identify Wacom as tablets for libwacom

* Tue Feb 21 2012 Peter Hutterer <peter.hutterer@redhat.com>
- Source file is .bz2, not .xz

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 0.3-1
- Update to 0.3

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-1
- Update to 0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.1-1
- Initial import (#768800)
