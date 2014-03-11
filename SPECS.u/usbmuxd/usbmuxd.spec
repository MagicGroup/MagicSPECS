Name:          usbmuxd
Version:       1.0.8
Release:       2%{?dist}
Summary:       Daemon for communicating with Apple's iPod Touch and iPhone

Group:         Applications/System
# All code is dual licenses as GPLv3+ or GPLv2+, except libusbmuxd which is LGPLv2+.
License:       GPLv3+ or GPLv2+ and LGPLv2+
URL:           http://marcansoft.com/uploads/
Source0:       http://marcansoft.com/uploads/usbmuxd/%{name}-%{version}.tar.bz2

BuildRequires: libplist-devel
BuildRequires: libusb1-devel
BuildRequires: cmake
Requires(pre): shadow-utils

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: usbmuxd = %{version}-%{release}
Requires: pkgconfig
Requires: libusb1-devel

%description devel
Files for development with %{name}.

%prep
%setup -q

# Set the owner of the device node to be usbmuxd
sed -i.owner 's/ATTR{idVendor}=="05ac"/OWNER="usbmuxd", ATTR{idVendor}=="05ac"/' udev/85-usbmuxd.rules.in
sed -i.user 's/-U usbmux/-U usbmuxd/' udev/85-usbmuxd.rules.in

%build
export CMAKE_PREFIX_PATH=/usr
%{cmake} -DUSB_INCLUDE_DIR=%{_includedir}/libusb-1.0 .

make %{?_smp_mflags}

%install
export CMAKE_PREFIX_PATH=/usr$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir  -p %{buildroot}%{_prefix}/lib/udev/
mv %{buildroot}/lib/udev/rules.d %{buildroot}%{_prefix}/lib/udev/

magic_rpm_clean.sh

%pre
getent group usbmuxd >/dev/null || groupadd -r usbmuxd -g 113
getent passwd usbmuxd >/dev/null || \
useradd -r -g usbmuxd -d / -s /sbin/nologin \
	-c "usbmuxd user" -u 113 usbmuxd
exit 0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1 README.devel
%{_prefix}/lib/udev/rules.d/85-usbmuxd.rules
%{_bindir}/iproxy
%{_sbindir}/usbmuxd
%{_libdir}/libusbmuxd.so.*

%files devel
%defattr(-,root,root,-)
%doc README.devel
%{_includedir}/*.h
%{_libdir}/libusbmuxd.so
%{_libdir}/pkgconfig/libusbmuxd.pc

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0.8-2
- 为 Magic 3.0 重建

* Mon Apr  9 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.8-1
- New stable 1.0.8 release

* Thu Feb  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.7-3
- Add debian patch for CVE-2012-0065. Fixes RHBZ 783523

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.7-1
- New stable 1.0.7 release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.6-1
- New stable 1.0.6 release

* Fri Jul 23 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-1
- New stable 1.0.5 release

* Fri May 28 2010 Bastien Nocera <bnocera@redhat.com> 1.0.4-3
- Fix udev rule to use the usbmuxd user

* Wed May 12 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.4-2
- Actually upload a source file

* Tue May 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.4-1
- New stable 1.0.4 release

* Mon Mar 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-1
- New stable 1.0.3 release

* Thu Feb 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-1
- New stable 1.0.2 release

* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 1.0.0-3
- Use the gid/uid reserved for usbmuxd in setup 2.8.15 and above

* Fri Jan 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-2
- Run deamon under the usbmuxd user

* Mon Dec  7 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-1
- New stable 1.0.0 release

* Sat Oct 31 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.1.rc2
- New 1.0.0-rc2 test release

* Thu Oct 29 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.2.rc1
- Add patch to fix install of 64 bit libs

* Tue Oct 27 2009 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.1.rc1
- New 1.0.0-rc1 test release

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 0.1.4-2
- Make usbmuxd autostart on newer kernels
- (Still doesn't exit properly though)

* Mon Aug 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.4-1
- Update to 0.1.4

* Tue Aug  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.3-1
- Update to 0.1.3, review input

* Mon Aug  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.2-1
- Update to 0.1.2

* Mon Aug  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.1-1
- Initial packaging
